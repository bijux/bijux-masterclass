---
module_id: DARCH-056
program: Data Architecture Engineering
level: 2
module_number: 56
title: Hierarchy Management
status: complete
last_verified: 2026-09-03
---

# Hierarchy Management

## One-Page Review

### Governing question

How should an enterprise model, govern, publish, change, and retire organizational, ownership, reporting, product, geography, account, classification, and other hierarchies without confusing one perspective with truth or corrupting rollups, history, and downstream decisions?

### Essential definitions

- A **hierarchy** is a named, typed, governed set of directed relationships interpreted as parent-child, broader-narrower, contains-contained, reports-to, owns-owned, or another declared ordering.
- A **hierarchy type** defines node types, edge meaning, permitted cardinality, structural constraints, temporal semantics, authority, and intended uses.
- A **node** is an identified entity, concept, account, grouping, or placement participating in a hierarchy.
- An **edge** is a direct typed relationship from parent to child with provenance, status, and effective interval.
- A **placement** is a node's occurrence under a parent in a hierarchy; one entity can have several placements in a polyhierarchy.
- A **tree** is an acyclic connected hierarchy with one root and exactly one parent for each nonroot node.
- A **forest** is a set of disjoint trees; a **directed acyclic graph** permits multiple parents but no directed cycle.
- A **polyhierarchy** permits a node or concept to have more than one parent or broader concept.
- **transitive closure** is the inferred ancestor-descendant relation produced from direct edges; it is derived state, not a replacement for asserted edges.
- A **rollup** aggregates facts from descendants according to hierarchy, allocation, time, and version.
- A **hierarchy release** is an immutable identified publication of nodes, direct edges, rules, provenance, and validation evidence.
- A **subtree move** closes one parent edge and opens another while preserving node identity and historical placement.

### Central model, mechanism, or theorem

Represent hierarchy architecture as:

`H = (outcomes, types, nodes, edges, constraints, time, versions, workflows, derivations, publication, protection, service, ownership, evidence, lifecycle)`

A hierarchy is valid only relative to its type and time. `reports_to`, legal ownership, management consolidation, geographic containment, product classification, and navigation may connect the same entities differently. Store direct typed edges with effective intervals and provenance. Derive ancestors, descendants, paths, depth, rollups, and materialized closure for a declared release. Structural rules—single parent, root count, acyclicity, allowed node types, ownership totals, or synchronized subtrees—belong to the hierarchy type rather than one universal graph validator.

### Critical invariants

- Every hierarchy names its type, purpose, consumers, node and edge semantics, authority, constraints, temporal rules, and retirement owner.
- Node identity remains separate from placement, label, display order, path, depth, and current parent.
- Direct asserted edges remain separate from inferred transitive relationships and cached paths.
- Self-links, duplicate edges, invalid node-type pairs, and prohibited cycles fail before publication.
- Tree, forest, DAG, polyhierarchy, and general graph rules are declared; one structure is not silently assumed for all uses.
- Effective time, transaction time, publication time, and consumer activation time remain distinct.
- Published releases are immutable; scheduled changes create new effective edge versions or releases.
- Reparent, move, merge, split, add, retire, and correction operations preserve prior paths, identifiers, provenance, and affected consumers.
- Rollups declare hierarchy release, fact time, allocation, shared-descendant policy, missingness, currency or unit, and reconciliation.
- Hierarchy APIs, events, snapshots, closure tables, and caches expose resolved version, freshness, completeness, and correction behavior.
- Protection follows nodes, edges, inferred relationships, ownership, reviewer notes, derived groups, histories, exports, and backups.
- Recovery restores rules, direct edges, versions, workflows, derivations, positions, permissions, and consumer evidence—not only current paths.

### Common failures

Common failures are using one hierarchy for every purpose; storing only `parent_id`; encoding path in node identity; overwriting an old parent; assuming every hierarchy is a tree; forbidding legitimate multiple parents or permitting them where rollups require exclusivity; deriving direct edges from closure; accepting cycles because the database allows them; validating only the changed edge rather than its component; attaching facts to display placements instead of stable entities; double-counting shared descendants; moving a subtree without impact analysis; using current hierarchy for historical reports; confusing effective and load time; letting label edits trigger identity changes; publishing partial closure as complete; allowing broad hierarchy browsing to reveal sensitive relationships; and retiring the service while reports, rules, caches, or histories remain.

### Compact example

Release 1 places `store-1` under `north` and `store-2` under `south`; leaf values are 40 and 60. Release 2 moves `store-1` to `south`. Under release 1, north and south roll up to 40 and 60. Under release 2, they roll up to 0 and 100 while root remains 100. Both releases pass cycle validation. The result is reproducible because the rollup names the hierarchy release and does not rewrite the earlier path.

### Connections

[DARCH-018](018-temporal-and-historical-modeling.md), [DARCH-023](023-data-ownership-and-accountability.md), [DARCH-026](026-data-products-and-service-expectations.md), [DARCH-051](051-master-data-and-golden-records.md), [DARCH-052](052-reference-data.md), and [DARCH-055](055-registry-consolidation-and-coexistence-styles.md) establish temporal, ownership, product, master, reference, and implementation boundaries. This module governs hierarchical relationships; [DARCH-057](../ROADMAP.md) next deepens controlled vocabularies.

## Governing Question

Hierarchies make data navigable and decisions computable. They determine who reports to whom, which products belong to a category, which legal entities consolidate, how territories roll up, which accounts compose a statement, and where responsibility or access inherits. A wrong edge can change money, access, risk, reporting, or accountability far beyond the row it occupies.

The governing question is which typed, temporal, versioned relationship system supports each decision while preserving competing perspectives, direct evidence, safe changes, reproducible rollups, correction, protection, recovery, and lifecycle closure.

## Why This Matters

The W3C [SKOS Reference](https://www.w3.org/TR/skos-reference/) distinguishes direct broader and narrower assertions from transitive super-properties, supports polyhierarchy, and discusses cycle detection as an application concern. The W3C [SKOS Primer](https://www.w3.org/TR/skos-primer/) illustrates direct and transitive hierarchical relations. These mechanisms apply to knowledge organization; enterprise ownership or reporting edges require their own semantics and constraints.

IBM [Hierarchy](https://www.ibm.com/docs/en/imdm/12.0.0?topic=domain-hierarchy) describes hierarchy search, nodes, parent-child relationships, and roles. Its [HIERARCHYREL](https://www.ibm.com/docs/en/imdm/14.0.0?topic=tables-hierarchyrel) documentation represents direct relationships and update evidence, while [Exploring and Working with Hierarchies](https://www.ibm.com/docs/en/ws-and-kc?topic=data-exploring-hierarchies) demonstrates governed roles for editing. Provider data structures illustrate capabilities, not universal hierarchy semantics.

SAP [Processing Hierarchies](https://help.sap.com/docs/SAP_MASTER_DATA_GOVERNANCE/db97296fe85d45f9b846e8cd2a580fbd/e849384af47f471994b35daf23bd5467.html?version=MDG91.latest) covers version-dependent, time-dependent, and synchronized hierarchies. SAP [Time Dependency of Master Data](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/5e23dc8fe9be4fd496f8ab556667ea05/790ad553088f4308e10000000a174cb4.html) demonstrates validity intervals. Oracle's [Account Hierarchy](https://docs.oracle.com/en/applications/siebel/siebel-crm/26.3/szcmm/c-Account-Hierarchy-aij1006604.html) describes multilevel organizational parent-child structure and restructuring behavior.

W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) provides a provenance vocabulary, and NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy lifecycle engineering. Hierarchy management is configuration control over consequential relationships and their derived effects.

## Prerequisites and Retrieval

You should understand graph basics, identifiers, master and reference data, source authority, temporal modeling, data products, APIs, events, aggregation, access control, lineage, reliability, recovery, and governance.

Retrieve hierarchy, hierarchy type, node, edge, direct relation, transitive relation, parent, child, ancestor, descendant, root, leaf, depth, path, tree, forest, DAG, polyhierarchy, cycle, placement, rollup, allocation, alternate hierarchy, effective time, transaction time, release, closure table, materialized path, subtree move, reparent, merge, split, orphan, synchronization, and retirement.

As a retrieval test, inspect “build the company hierarchy.” Ask whether it means legal ownership, financial consolidation, management reporting, sales territory, access inheritance, brand structure, or navigation; which entities and relationships; whether multiple parents, cycles, allocations, and future changes are valid; the effective time; consumers; consequences; owner; and exit conditions. “The” hierarchy usually hides several products.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish node identity, placement, direct edge, inferred ancestry, path, label, and presentation order;
2. define hierarchy types by purpose, node and edge semantics, structural constraints, time, authority, and consumers;
3. compare trees, forests, DAGs, polyhierarchies, general graphs, alternate perspectives, and synchronized subhierarchies;
4. model bitemporal direct edges, immutable releases, scheduled changes, corrections, and consumer activation;
5. validate roots, parent cardinality, cycles, allowed types, reachability, allocations, and domain-specific constraints;
6. design subtree move, reparent, add, retire, merge, split, approval, conflict, and rollback workflows;
7. compute rollups without double counting and reproduce results against pinned hierarchy and fact versions;
8. publish direct, ancestor, descendant, path, change, and bulk contracts with cache and closure semantics;
9. protect inferred relationships and operate hierarchy services through scale, failure, reconciliation, and recovery; and
10. assign ownership, measure decision outcomes, migrate consumers, and verify retirement.

## Core Exposition

**Start with the decision.** Name what the hierarchy enables: consolidation, navigation, responsibility, routing, aggregation, eligibility, access, reporting, or analysis.

The same edge shape can mean different things. `owns`, `reports_to`, `broader_than`, and `located_in` have different authority, transitivity, time, and risk.

**Define a hierarchy type.** Specify hierarchy ID, purpose, node types, edge type, direction, roots, parent cardinality, cycle policy, depth, ordering, time, owner, and consumers.

Do not reuse a generic “parent-child” table without preserving relationship semantics. The type is part of every edge identity.

**Separate entity from placement.** A product, organization, or concept has stable identity. Its placement records participation under a parent in a particular hierarchy and interval.

One entity can occur in several hierarchies or several branches. A path or parent is not a durable entity identifier.

**Use stable node identifiers.** Node IDs should not encode current parent, depth, display sequence, region, or label.

Subtree moves then change edges rather than node identity. Consumers can follow the same entity across reorganization.

**Model direct edges as assertions.** Store hierarchy, type, parent, child, relation, source, authority, effective interval, transaction interval, status, operation, and provenance.

Direct edges are the governed input. Ancestors, descendants, paths, depths, and closure are derived for a declared version.

**Separate direct and transitive relations.** `A` directly contains `B`, and `B` directly contains `C`; `A` transitively contains `C`.

Do not persist the inferred relation as if it were independently asserted. Keep derivation version so closure can be rebuilt and checked.

**Choose tree semantics only when justified.** A tree requires one root, one parent per nonroot node, connectedness, and acyclicity.

Legal ownership for a declared consolidation perimeter may approximate a tree; concept classification and matrix reporting often do not.

**Use forests explicitly.** Separate roots can represent independent legal groups, disconnected regions, provisional imports, or several charts.

Do not attach artificial roots without declaring their meaning. A technical grouping node can affect depth, rollup, and consumer interpretation.

**Use DAGs for legitimate multiple parents.** Polyhierarchies let a product belong under both material and use categories or an employee participate in matrix structures.

Multiple paths change query and aggregation behavior. Consumers must know whether reachability, placement, or unique entity membership is intended.

**Use general graphs when hierarchy is the wrong abstraction.** Peer, supplier, dependency, collaboration, and network relationships can be cyclic and nontransitive.

Forcing them into parent-child semantics creates false inheritance. Publish them as typed graph relations instead.

**Define cycle policy by type.** Most rollup, ownership, containment, and reporting hierarchies prohibit directed cycles. Some conceptual systems may tolerate them while warning consumers.

Validate before publication and after the complete proposed change. A locally valid edge can close a distant path into a cycle.

**Check self-links and duplicates.** An edge from a node to itself is usually invalid even before transitive closure. Duplicate active edges can double-count or confuse provenance.

Define whether two authorities can assert the same relationship separately. If so, preserve assertions but derive one governed edge with lineage.

**Validate node-type pairs.** A region may contain locations, a legal entity may own subsidiaries, and an account group may contain accounts.

Prevent impossible pairs such as product category reporting to employee unless the hierarchy type explicitly permits heterogeneous nodes.

**Validate parent cardinality.** A tree permits one active parent. A DAG permits several. A legal ownership hierarchy may permit several owners but require percentages.

Check cardinality at effective time, not merely across stored history. Closed and future edges should not create false violations.

**Validate roots and reachability.** Some hierarchies require every active node to reach exactly one authorized root. Others allow orphans or several roots.

Model orphan, pending placement, excluded, retired, and source unavailable as typed states. Do not attach unknown nodes arbitrarily to make validation green.

**Bound depth and breadth when operationally relevant.** Deep chains can overflow consumers or make access and rollups expensive. Very broad nodes can create oversized responses and review work.

Set domain or service constraints with evidence. Do not confuse an implementation limit with a semantic law.

**Preserve sibling order separately.** Display order, ranking, and navigation sequence are edge or placement metadata, not identity.

Concurrent insertions need deterministic order keys and conflict handling. Reordering should not trigger false entity changes.

**Model edge attributes.** Ownership percentage, allocation weight, relationship role, consolidation method, confidence, source, and effective time can qualify an edge.

Do not hide these in node attributes. The same child can have different roles or weights under different parents.

**Separate structural and semantic validation.** Structural checks cover IDs, types, cardinality, roots, cycles, connectivity, and interval form.

Semantic checks cover whether the relationship is true and authorized, weights are meaningful, legal requirements hold, and intended decisions remain valid.

**Use temporal edges.** Close old edge `[start, move_time)` and open new edge `[move_time, end)` rather than overwriting a parent.

Half-open intervals avoid double placement at the boundary. Declare calendar, time zone, precision, and rules for backdated corrections.

**Separate temporal axes.** Effective time describes when the relationship applies. Transaction time records when the system learned or changed it.

Publication time and consumer activation can differ again. Historical truth, late correction, future schedule, and operational replay need these distinctions.

**Publish immutable releases.** A release binds hierarchy metadata, node versions, direct edge versions, constraints, source positions, approvals, validation, and manifest.

Corrections create a new release or versioned amendment. Silent edits make reports and access decisions irreproducible.

**Support planned hierarchies.** Future reorganizations, budgets, territories, or classification changes can be modeled in planning versions without becoming current early.

Control who can view and edit plans. Planned organizational edges can be highly sensitive.

**Support alternate hierarchies.** Legal, management, financial, sales, risk, and analytical perspectives may all be valid for the same entities.

Name each product and prohibit silent substitution. A financial report must not default to the current sales hierarchy.

**Control synchronized subhierarchies.** Some subtrees appear in several views and must move together; others are intentionally independent.

Define synchronization source, direction, scope, operation ID, version, conflict, and failure. Copying a subtree without a contract creates drift.

**Design proposal and approval workflow.** A change request identifies hierarchy, affected nodes and edges, reason, authority, effective time, consumers, expected version, and impact.

Reviewers need structural validation, semantic evidence, before-and-after paths, rollup effects, protection impact, and rollback plan.

**Use expected-version updates.** A move approved against release 12 should not apply after another change produces release 13 without revalidation.

Reject stale operations or rebase them visibly. Last-write-wins can reintroduce a removed edge or cycle.

**Give operations stable identity.** Add, move, reorder, merge, split, synchronize, and retire commands carry operation ID, initiator, authority, expected version, effective time, and idempotency key.

On unknown outcome, query operation state before retry. Duplicate commands must not duplicate edges or close intervals twice.

**Validate the proposed graph atomically.** Apply a change to an isolated candidate version, then check all structural and semantic rules before publication.

Multi-edge changes such as subtree move need one coherent boundary. Removing before adding or adding before removing can expose invalid intermediate state.

**Treat subtree moves as high-impact changes.** A single direct edge can change paths for thousands of descendants and every inherited fact or permission.

Calculate descendant count, affected ancestors, rollups, policies, reports, caches, access, and consumers before approval.

**Distinguish move from copy.** A move closes old placement and opens new placement. A copy adds another placement where polyhierarchy permits it.

Interface language and operations must make the difference clear. Accidental copy can double-count; accidental move can remove valid reachability.

**Treat node merge and split separately from entity resolution.** Merging hierarchy nodes can combine categories or placements without claiming their underlying entities are identical.

Define identifier, edge, child, fact, alias, and historical behavior. A split may require allocation evidence unavailable in old facts.

**Retire rather than erase.** A retired node or edge stops future use but remains resolvable for historical data according to retention policy.

Publish replacement or alias only when semantically justified. One node can split into several with no deterministic replacement.

**Design rollups explicitly.** State fact grain, attachment key, fact time, hierarchy release, inclusion rule, aggregation function, currency or unit, allocation, and missingness.

“Sum by parent” is unsafe without these dimensions. The hierarchy and facts form one reproducibility contract.

**Avoid double counting in polyhierarchies.** A leaf reachable through two paths can be counted twice if aggregation follows placements blindly.

Choose unique-entity rollup, path-specific allocation, explicit weights, primary placement, or deliberate repeated counting. Name the policy in output metadata.

**Validate allocation weights.** Ownership or management weights may need to total one for a child at an effective time, or follow domain-specific consolidation rules.

Do not normalize bad weights automatically without recording the correction. Missing or disputed allocation can require unresolved output.

**Handle nonadditive facts.** Balances, distinct customers, ratios, statuses, and averages cannot always be summed through hierarchy levels.

Define aggregation algebra and required numerator, denominator, snapshot, or deduplication state. Hierarchy correctness does not prove measure additivity.

**Reconcile root and branch totals.** Compare leaf coverage, allocated totals, orphan facts, duplicate reachability, excluded nodes, and prior releases.

Large changes can be legitimate after reorganization; reconciliation must explain them rather than merely enforce equality.

**Attach facts to stable identities.** Store facts against entity, account, product, or placement according to business meaning, not a mutable textual path.

Resolve the appropriate hierarchy as of fact or reporting time. Reorganizing presentation should not rewrite base facts silently.

**Choose historical reporting policy.** Restated reporting applies a newer hierarchy to older facts; as-was reporting uses the hierarchy effective then.

Both can be legitimate. Label outputs with policy and release so consumers do not compare incompatible totals.

**Publish direct-edge APIs.** Support hierarchy and release selection, node lookup, direct parents and children, edge metadata, effective-time query, pagination, and typed errors.

Do not return “the parent” where multiple parents are possible. Include resolved release and completeness.

**Publish traversal APIs deliberately.** Ancestor, descendant, path, common-ancestor, and subtree operations need depth bounds, cycle protection, ordering, pagination, authorization, and resource limits.

Expose whether results use asserted edges, inferred closure, or cached materialization and which version produced them.

**Publish snapshots for bulk consumers.** Provide hierarchy metadata, nodes, direct edges, optional closure, schemas, manifests, digests, validation summary, and release notes.

Consumers verify and activate atomically. Mixing nodes from one release and closure from another must fail visibly.

**Publish change events.** Node-added, edge-added, edge-closed, subtree-moved, reordered, merged, split, corrected, release-published, and retired have different semantics.

Include prior and new release, operation, affected root, effective time, cause, ordering key, idempotency, and protection classification.

**Use events with snapshots.** Events provide change notification and incremental maintenance; snapshots establish or repair complete state.

Define retention, gap detection, replay, compaction, schema compatibility, and reconciliation. A consumer missing one move can corrupt a whole subtree.

**Treat closure tables as derived indexes.** Materialized ancestor-descendant rows accelerate traversal and rollups but can become stale or partially updated.

Version closure with its direct-edge release, build atomically, validate counts and cycles, and rebuild from authoritative edges during recovery.

**Treat materialized paths as derived presentation.** Paths speed prefix queries but change for every descendant during a move.

Do not use them as stable identifiers. Update atomically or publish a new generation so consumers never see mixed paths.

**Control cache invalidation by impact.** One edge move invalidates the moved node, descendants, old and new ancestors, paths, rollups, and authorization decisions.

Use hierarchy and release keys where possible. Broad time-to-live alone can leave dangerous stale inheritance.

**Engineer for graph scale.** Observe nodes, edges, roots, depth, width, components, path multiplicity, hot subtrees, change fan-out, closure size, and traversal cost.

Use bounded queries, indexes, precomputation, batching, partitioning, and backpressure. Preserve correctness when a result is truncated.

**Control concurrent edits.** Independent branch changes may commute; moves involving shared ancestors, synchronized subtrees, or global constraints may conflict.

Use expected releases and semantic conflict detection rather than one global lock when scale requires concurrency.

**Design degraded behavior.** If closure is stale, serve direct edges with a warning, pin the last verified release, queue changes, or stop a high-consequence rollup.

Do not infer ancestry from partially rebuilt state. Degraded policy follows consumer consequence.

**Protect hierarchy inference.** Reporting lines, beneficial ownership, household structure, planned reorganizations, risk groupings, and access ancestry can be sensitive.

Apply purpose, minimization, row and edge authorization, query controls, inference review, encryption, audit, retention, deletion, and export limits.

**Prevent enumeration.** Traversal APIs can reveal whole organizations or relationship networks from one known node.

Authorize each requested view, cap breadth and depth, rate-limit, monitor query patterns, and avoid leaking hidden counts or labels in errors.

**Separate access hierarchy from descriptive hierarchy.** A reporting or organizational parent should not automatically grant authorization inheritance.

Model access edges and policies separately unless the organization explicitly governs the coupling and tests change impact.

**Plan correction propagation.** A bad edge may have affected reports, pricing, territory assignment, permissions, risk, models, and decisions.

Publish correction scope, prior and new release, effective and transaction time, affected descendants, replay guidance, and consumer acknowledgement.

**Recover the whole hierarchy system.** Restore type rules, node and direct-edge history, releases, source positions, proposals, approvals, operations, aliases, closure build definitions, permissions, events, and audit.

Rebuild derived paths and closure, verify cycles and keyed edges, then reconcile consumers. A current adjacency list alone is insufficient.

**Assign ownership precisely.** Domain owners define relationship meaning; source owners maintain assertions; hierarchy-product owners publish; stewards run governed changes.

Platform, reporting, finance, security, privacy, legal, records, reliability, consumer, incident, and retirement owners retain their decisions.

**Measure outcomes and harms.** Track invalid edges, cycles blocked, orphans, change lead time, stale consumers, rollup reconciliation, access incidents, correction time, adoption, decision outcomes, and cost.

Node and edge counts show scale, not usefulness. Tie the hierarchy to the decisions it changes.

**Migrate by version and contract.** Compare old and new node identity, direct edges, histories, roots, paths, rollups, APIs, events, permissions, and consumers.

Use shadow releases and cohort activation. Preserve old identifiers or governed aliases and keep as-was reporting until retention permits closure.

**Retire with evidence.** Inventory sources, types, nodes, edges, releases, closure, paths, rules, workflows, events, files, APIs, caches, reports, policies, models, credentials, backups, and duties.

Stop authoring and publication only after consumers migrate, retained history has custody, access is revoked, prohibited copies are deleted, and restore cannot resurrect unsupported hierarchies.

## Definitions and Notation

Let direct edge version be $e=(H,T,p,c,r,t_e,t_o,s,P)$ with hierarchy $H$, type $T$, parent $p$, child $c$, role or attributes $r$, effective interval $t_e$, transaction interval $t_o$, status $s$, and provenance $P$.

For release $v$, direct edge set $E_v$ induces reachability $E_v^+$ but does not turn inferred ancestor relations into asserted edges. Define:

$$
Acyclic(E_v) \iff \nexists n : (n,n) \in E_v^+.
$$

For a strict tree at time $t$, there is one root with indegree zero, every other active node has indegree one, all nodes are reachable from the root, and $E_t$ is acyclic.

Let rollup for parent $p$ be:

$$
R(p,v,t)=Aggregate(\{f(x,t)\cdot w(path,x,p,v,t)\}),
$$

where fact version, hierarchy release, time, path or unique-node policy, allocation $w$, units, and missingness are declared.

Define `FitHierarchy(H,u,t)` as a review predicate requiring justified purpose, typed semantics, stable identities, valid direct edges, explicit time and releases, safe workflows and derivations, protected and recoverable publication, accountable outcomes, and lifecycle closure for use $u$ at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten architecture gates.

**1. Outcome gate.** Name hierarchy-dependent decisions, consumers, deadlines, harms, fallback, value, and assurance depth.

**2. Type gate.** Define hierarchy, node and edge semantics, direction, structural family, roots, cardinality, cycles, depth, ordering, time, and authority.

**3. Evidence gate.** Preserve stable node IDs, direct typed edges, source assertions, effective and transaction time, operation, approval, and provenance.

**4. Integrity gate.** Validate self-links, duplicates, type pairs, roots, reachability, parent cardinality, cycles, allocations, and domain rules on the proposed graph.

**5. Version gate.** Publish immutable releases, planned versions, corrections, manifests, source positions, validation, consumer activation, and historical resolution.

**6. Workflow gate.** Control add, move, copy, reorder, synchronize, merge, split, retire, override, expected versions, idempotency, conflict, and rollback.

**7. Derivation gate.** Define paths, closure, depth, rollups, allocation, shared descendants, nonadditive facts, as-was or restated policy, and reconciliation.

**8. Contract gate.** Publish direct and inferred queries, snapshots, events, caches, pagination, bounds, freshness, completeness, corrections, and consumer duties.

**9. Protection and service gate.** Bound access, inference, enumeration, planned changes, scale, hot subtrees, fan-out, degraded behavior, incidents, and recovery.

**10. Lifecycle gate.** Assign ownership, measure outcomes and cost, migrate versions and consumers, transfer custody, and verify retirement.

Passing these gates supports one hierarchy use. It does not prove that the same structure fits another purpose, that all hierarchical relations are transitive, or that a valid graph produces a correct business rollup.

### Executable evidence

The executable example validates two acyclic releases and reproduces rollups before and after a subtree move.

<!-- bijux-verify: {"id":"temporal-hierarchy-move-rollup","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"release_1_north=40\nrelease_1_south=60\nrelease_2_north=0\nrelease_2_south=100\nrelease_2_root=100\ncycle_detected=false\nreleases=2\n","stderr":""}} -->
```python
releases = {
    1: [("root", "north"), ("root", "south"), ("north", "store-1"), ("south", "store-2")],
    2: [("root", "north"), ("root", "south"), ("south", "store-1"), ("south", "store-2")],
}
facts = {"store-1": 40, "store-2": 60}


def descendants(edges, node):
    children = [child for parent, child in edges if parent == node]
    return set(children).union(*(descendants(edges, child) for child in children))


def has_cycle(edges):
    nodes = {node for edge in edges for node in edge}
    return any(node in descendants(edges, node) for node in nodes)


def rollup(edges, node):
    return sum(facts.get(child, 0) for child in descendants(edges, node))


print(f"release_1_north={rollup(releases[1], 'north')}")
print(f"release_1_south={rollup(releases[1], 'south')}")
print(f"release_2_north={rollup(releases[2], 'north')}")
print(f"release_2_south={rollup(releases[2], 'south')}")
print(f"release_2_root={rollup(releases[2], 'root')}")
print(f"cycle_detected={str(any(has_cycle(edges) for edges in releases.values())).lower()}")
print(f"releases={len(releases)}")
```

The result proves only recursive reachability, cycle checks, and integer sums for two small in-memory trees. It does not prove edge truth, authority, temporal correctness, aggregation fitness, allocation, concurrency, scale, consumer activation, protection, recovery, or safe production change.

## Alternatives and Trade-Offs

**Single tree.** Queries and exclusive rollups are simple, but multiple legitimate parents and perspectives may be lost.

**Forest.** Independent roots and provisional populations remain explicit, while consumers must handle more than one top-level scope.

**DAG or polyhierarchy.** Multiple classifications or reporting paths are represented honestly, but paths, rollups, access, and double counting become harder.

**General typed graph.** Rich relationships avoid false hierarchy semantics, at the cost of weaker inherited operations and more complex queries.

**Adjacency list.** Direct-edge writes and provenance are simple; recursive traversal and large rollups may be expensive.

**Closure table.** Ancestor queries are fast; change fan-out, derived-state integrity, storage, and versioning cost increase.

**Materialized path.** Prefix queries and display are convenient; subtree moves rewrite many paths and paths must not become identity.

**Nested sets.** Read-heavy subtree queries can be efficient; concurrent inserts and moves are costly and temporal history is awkward.

**Live traversal.** Results reflect direct current edges and avoid stale closure; deep or broad queries need strict resource control.

**Immutable release.** Reproducibility and atomic activation improve while urgent change requires a new release and consumers can lag.

**As-was rollup.** Historical organization is preserved, but comparisons across time include structural change.

**Restated rollup.** Current structure makes comparison easier, but it rewrites historical grouping and needs prominent labeling.

Choose by relationship semantics, parent cardinality, cycle policy, temporal needs, change rate, read patterns, rollup algebra, protection, scale, recovery, consumer migration, and exit.

## Failure Modes and Misconceptions

1. **Every parent-child relation is the same.** Ownership, reporting, containment, classification, and navigation carry different semantics.
2. **A hierarchy is always a tree.** Forests, DAGs, polyhierarchies, and general graphs are common.
3. **The parent belongs on the node.** Placement is a relationship with its own time and provenance.
4. **A path is a stable identifier.** Paths change when any ancestor moves.
5. **Direct edges are transitive.** Direct assertions and inferred reachability are distinct.
6. **Acyclicity is universal.** Many hierarchy uses require it, but the type must declare the rule.
7. **Local edge validation prevents cycles.** A distant existing path can close the cycle.
8. **Multiple parents only affect display.** They change reachability, rollups, access, and counts.
9. **Moving one edge is a small change.** Every descendant and inherited decision can move.
10. **Current hierarchy explains history.** Reports need pinned as-was or explicitly restated policy.
11. **Valid hierarchy means valid rollup.** Fact grain, aggregation, allocation, units, and missingness also matter.
12. **Summing each path is safe.** Shared descendants can be counted more than once.
13. **Closure is authoritative data.** It is derived from versioned direct edges.
14. **Publishing an event updates every consumer.** Gap detection, activation, reconciliation, and acknowledgement remain.
15. **Organizational hierarchy should drive access.** Access inheritance needs separate explicit governance.
16. **A read-only hierarchy is nonsensitive.** Relationships and inferred groups can expose protected information.
17. **A backup of current edges is recovery.** Rules, histories, workflows, closure definitions, permissions, and events also matter.
18. **Turning off editing retires the hierarchy.** APIs, files, caches, reports, policies, histories, and obligations remain.

## Worked Examples

### Example 1

Legal ownership and management reporting connect the same subsidiaries differently. Each hierarchy has its own type, authority, release, and consumers. **Conclusion:** alternative perspectives must be named, not reconciled into one false tree.

### Example 2

A product appears beneath both “recycled materials” and “outdoor use.” Search traverses both paths, while sales rollup uses a primary placement. **Conclusion:** polyhierarchy needs consumer-specific counting policy.

### Example 3

A proposed edge from division A to root would close an existing root-to-A path. Candidate-release validation rejects the cycle before publication. **Conclusion:** validate the complete prospective graph.

### Example 4

A regional reorganization closes `north → store-1` at day 10 and opens `south → store-1` at day 10. Historical day-9 reports retain the northern placement. **Conclusion:** moves create temporal edge versions.

### Example 5

One ownership edge has 60% weight and another 40%. The system validates the child's effective weights total 100% before a consolidation release. **Conclusion:** edge attributes can carry domain invariants.

### Example 6

A unique customer count is attached to two shared category paths. The report deduplicates stable customer IDs at the requested ancestor instead of summing child counts. **Conclusion:** nonadditive measures require their own rollup algebra.

### Example 7

A subtree move changes 25,000 descendant paths and 300 access rules. The workflow shadows rollups and authorization effects before approval. **Conclusion:** direct edge count understates change impact.

### Example 8

A consumer misses an `edge-closed` event but receives the later `edge-added` event. Snapshot reconciliation detects dual placement and repairs the local copy. **Conclusion:** events need complete-state recovery.

### Example 9

A planned acquisition hierarchy is visible only to a restricted group; even node counts and traversal errors avoid revealing the structure. **Conclusion:** hierarchy metadata and inference can be sensitive.

### Example 10

No one edits a retired chart, but historical financial reports, model features, cache snapshots, and backup recovery still resolve its releases. **Conclusion:** retirement requires consumer and retained-history closure.

## Cross-Program Connections

- **Data engineering:** temporal edges, change capture, graph processing, closure builds, rollups, snapshots, events, reconciliation, replay, and history implement hierarchy products.
- **Platform engineering:** graph and relational stores, workflow, APIs, eventing, caches, policy, observability, recovery, tenancy, and safe releases support operation.
- **API and service engineering:** direct and transitive queries, bounded traversal, version selection, expected versions, idempotency, events, correction, and deprecation shape contracts.
- **Security and privacy:** ownership, reporting, household, access, planned changes, inference, enumeration, row and edge controls, retention, deletion, and audit constrain publication.
- **Analytics engineering:** dimensions, slowly changing structures, bridge tables, allocations, restatement, nonadditive measures, and reconciliation depend on hierarchy semantics.
- **Machine learning:** hierarchical labels, features, evaluation slices, graph embeddings, leakage, drift, and historical reproducibility require pinned versions.
- **Organizational design:** legal, management, responsibility, decision rights, stewardship, approval, escalation, and funding create real hierarchy authority.
- **Reliability engineering:** hot subtrees, traversal bounds, cache invalidation, change fan-out, event gaps, degraded modes, recovery, and correction time define service.
- **Economics and decision science:** aggregation error, reorganization cost, value of alternate views, change externalities, option value, and exit cost guide investment.
- **Systems engineering:** boundaries, interfaces, configurations, hazards, change impact, assurance, lifecycle, and verification frame the hierarchy system.

## References

1. W3C, *SKOS Simple Knowledge Organization System Reference*. <https://www.w3.org/TR/skos-reference/>
2. W3C, *SKOS Simple Knowledge Organization System Primer*. <https://www.w3.org/TR/skos-primer/>
3. IBM, *Hierarchy*. <https://www.ibm.com/docs/en/imdm/12.0.0?topic=domain-hierarchy>
4. IBM, *HIERARCHYREL*. <https://www.ibm.com/docs/en/imdm/14.0.0?topic=tables-hierarchyrel>
5. IBM, *Exploring and Working with Hierarchies in IBM Master Data Management*. <https://www.ibm.com/docs/en/ws-and-kc?topic=data-exploring-hierarchies>
6. SAP, *Processing Hierarchies*. <https://help.sap.com/docs/SAP_MASTER_DATA_GOVERNANCE/db97296fe85d45f9b846e8cd2a580fbd/e849384af47f471994b35daf23bd5467.html?version=MDG91.latest>
7. SAP, *Time Dependency of Master Data*. <https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/5e23dc8fe9be4fd496f8ab556667ea05/790ad553088f4308e10000000a174cb4.html>
8. Oracle, *Account Hierarchy*. <https://docs.oracle.com/en/applications/siebel/siebel-crm/26.3/szcmm/c-Account-Hierarchy-aij1006604.html>
9. W3C, *PROV-O: The PROV Ontology*. <https://www.w3.org/TR/2013/REC-prov-o-20130430/>
10. NIST, *SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems*. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Design hierarchy architecture for legal entities, products, accounts, territories, organizations, or concepts. Define type, nodes, edges, structure, time, authority, workflows, derivations, contracts, protection, service, ownership, and lifecycle.

### Exercise 2

A product taxonomy permits multiple parents, but finance wants exclusive category totals. Design placement and rollup semantics that preserve both needs.

### Exercise 3

A scheduled subtree move affects 80,000 descendants, reporting, pricing, and authorization. Design validation, impact analysis, publication, rollback, and correction.

### Exercise 4

An ownership hierarchy receives late backdated corrections while monthly reports have already published. Design bitemporal history and as-was versus restated reporting.

### Exercise 5

An organization plans to retire a hierarchy platform after moving products to domain services. Define evidence that authoring, derivation, consumers, protection, history, and correction duties moved or ended.

## Answers to the Exercises

### Answer 1

Name the decisions and whether the relation means owns, reports to, contains, broader than, allocates to, or another type. Define node types, stable IDs, direct edge direction, roots, parent cardinality, cycle policy, depth, ordering, allowed pairs, temporal axes, authority, and source provenance. Keep node identity separate from placement and asserted edges separate from derived paths and closure. Decide whether the structure is a tree, forest, DAG, polyhierarchy, or general graph based on semantics.

Publish immutable releases with direct edge histories, manifests, constraints, approvals, and source positions. Use expected-version idempotent workflows for add, move, copy, reorder, merge, split, synchronize, and retire. Define facts, allocation, unique-node or path counting, nonadditive measures, as-was or restated rollups, and reconciliation. Contract direct and inferred APIs, snapshots, events, caches, freshness, completeness, and correction. Protect inference and plans, bound traversal and change fan-out, recover rules and evidence, assign owners, measure outcomes, migrate consumers, and verify closure.

### Answer 2

Keep one product identity and permit several typed placements in the taxonomy DAG. Preserve direct parent edges, provenance, effective intervals, and hierarchy release. Navigation and search can traverse every placement. Finance must not sum each path because a product reachable twice would double-count. Define either a primary financial placement, explicit allocation weights across qualifying parents, or a separate exclusive financial hierarchy mapped from the taxonomy. The choice follows financial meaning rather than UI convenience.

Pin facts, taxonomy release, financial mapping or hierarchy, effective time, and aggregation rule in each output. Validate allocations total the required amount at each interval, identify unmapped and disputed products, and reconcile unique leaf coverage and branch totals. If taxonomy changes, publish a new release and impact report; do not rewrite old placements. Label taxonomy counts and financial totals as different products. Consumers needing both can trace the stable product and placement evidence without assuming that all hierarchical paths have additive semantics.

### Answer 3

Create an isolated candidate release using the expected current version. Close the old direct edge and open the new edge at one effective boundary. Validate IDs, types, roots, parent cardinality, cycles, reachability, depth, synchronized subtrees, allocations, and domain rules against the complete candidate graph. Enumerate descendants, old and new ancestors, paths, closure rows, rollups, prices, permissions, caches, events, reports, models, and consumer bindings. Shadow representative and full critical derivations and obtain domain, reporting, pricing, security, privacy, operational, and consumer approval.

Publish an immutable release with operation ID, prior release, effective time, manifest, change set, validation, and rollback plan. Activate by cohort or scheduled atomic version, invalidate versioned caches, and send idempotent events with snapshot repair available. Monitor consumer activation and reconcile keyed edges, paths, totals, and access results. Rollback is a new effective change if decisions already occurred under the moved structure; preserve both releases and correct downstream effects. If an edge was wrong, publish correction time and scope and verify each affected consumer repaired results.

### Answer 4

Store each direct ownership assertion with effective interval and transaction interval. The original edge remains the state believed when the monthly report ran. A later correction creates a new transaction-time version whose effective interval reaches into the prior month; it does not erase the earlier record. Capture source, authority, evidence, correction reason, approver, operation, and supersession. Validate percentage totals, cycles, roots, and consolidation rules across affected effective intervals.

An as-was report resolves the hierarchy version and facts available at the report's cutoff, reproducing the published result. A restated report uses corrected effective-time edges and a declared later knowledge cutoff. Give each report hierarchy release, fact release, time policy, allocation and consolidation rules, currency or unit, and reconciliation. Quantify affected entities and totals, publish correction notes, and preserve the original report. Consumer contracts must not silently replace as-was results with restated values; both can coexist with explicit labels and governance.

### Answer 5

Inventory every hierarchy type, node namespace, direct edge and history, source, authority, rule, planned version, release, workflow, approval, operation, alias, closure table, materialized path, allocation, rollup, API, event, snapshot, cache, report, access policy, model feature, consumer, credential, backup, retention rule, deletion path, and incident duty. For each authoring and derived capability, name the receiving domain service and verify its semantics, ownership, contract, protection, service objective, recovery, funding, and escalation—or prove it is no longer needed.

Run old and new products in bounded comparison across nodes, direct edges, temporal queries, cycles, roots, paths, rollups, events, access, and histories. Migrate consumers by cohort, including annual, offline, manual, and disaster-recovery users. Freeze and transfer authoring at explicit versions, drain changes, preserve required releases under named custody, revoke access, remove prohibited copies, and exercise correction and recovery without the old platform. Test that old jobs, caches, files, or backup restores cannot resurrect unsupported hierarchy state before accountable retirement.
