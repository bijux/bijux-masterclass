# Worked Answers — Module 02: Catalog, Ownership Graph, and Metadata Authority

Use these solutions to audit your reasoning for **Catalog, Ownership Graph, and Metadata Authority**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. What makes catalog metadata authoritative?

Authority comes from a declared source and owner, not from being displayed centrally. The catalog should ingest owner-maintained descriptors, validate them, record freshness, and expose derived relations without pretending that its cached copy created the fact.

The chapter’s decisive distinction is this: Metadata should live near the source that can maintain it. A component descriptor in source control is authoritative for its owner-declared relationships. The contract registry is authoritative for released bytes and digests. The identity directory is authoritative for group membership. Runtime discovery is authoritative for current instances. The catalog assembles these facts and records provenance; it does not magically become the creator of every fact it displays.

## 2. Why is owner a relation rather than a free-text email?

A stable group entity supports membership, escalation, history, and machine checks. Free-text contact data becomes stale and cannot reliably connect ownership across components, APIs, and resources.

In the cumulative capstone, the rule becomes concrete: Every active component, API, resource, system, and domain points to a group entity. The group is not only an email address. It has membership, escalation, and continuity when individuals change. The platform team validates that the owner exists; the organization determines who belongs to the group.

## 3. What is an orphan API?

An API with no accountable owner or no implementing component. It may have a contract file, but nobody is responsible for semantics, operation, change, or retirement.

A useful way to reason about the boundary is: An inverse edge can be generated for navigation, but the original declaration retains authority. Avoid generic dependsOn for everything. A service consuming an API has compatibility obligations; a service using a database has operational and data obligations. Collapsing these prevents useful policy.

## 4. Why must entity identity be canonical?

Canonical kind, namespace, and name prevent duplicate aliases and ambiguous references. Without canonical identity, ownership, dependency, and policy evidence can attach to different records that appear to describe the same thing.

The implementation consequence is: The capstone uses kind:namespace/name. Names are lowercase and stable. Titles may change; identity should not. Renaming an entity is a migration with aliases and consumer impact, not a cosmetic edit. Canonical references prevent analysis-api, Analysis API, and analysis http from becoming three policy subjects.

## 5. Should the catalog own the contract bytes?

The registry owns published immutable artifacts. The catalog references the active release and owner. Combining inventory and artifact storage can work technically, but their authorities and lifecycle rules remain distinct.

The important nuance is: A software catalog is a graph of identified entities and relationships, not a list of service names. The capstone models domains, systems, groups, components, APIs, and resources. Each entity has a canonical reference such as api:default/analysis-http. Components declare provided and consumed APIs; resources remain distinct from API boundaries.

## 6. What is the danger of inferred ownership?

Inference from repository names or commit history can seed a review, but silently treating it as authoritative can assign responsibility to the wrong team. Ownership needs explicit confirmation.

Under concurrency or failure, the distinction becomes: An API with a dissolved team is not “temporarily ownerless.” It is an incident and lifecycle risk. Block new releases, route escalation to the system owner, and establish an explicit transfer. Do not silently assign everything to the platform team: that hides organizational debt and turns the platform into the owner of facts it cannot safely operate.

## 7. How are dependencies different from API consumption?

A component may depend on a database or object store without consuming an API. API consumption is a contract relationship; resource dependency is an operational relationship. Both matter but imply different ownership and change risks.

The design remains honest only if: Derived facts must be labeled. “Component A consumes API B” may be declared by A, inferred from gateway traffic, or observed from runtime telemetry. These are different evidence classes. An inferred relation can trigger review but should not overwrite owner-declared intent without a policy.

## 8. Why track lifecycle in the catalog?

Discovery must distinguish proposed experiments from active supported interfaces and deprecated or retired ones. Without lifecycle, consumers can adopt unsupported or dying APIs.

The consumer-facing consequence is: Backstage’s descriptor format defines the shape of catalog entities, while its catalog graph illustrates ownership, inventory, lifecycle, dependency mapping, and API exposure. Use those concepts as a model, not as permission to hide authoritative sources.

**Evidence.** Reconcile catalog relations with source-owned metadata and verify immutable digest-addressed publication, authority, idempotent replay, and changed-byte rejection.

## 9. What should happen to stale metadata?

The platform should expose freshness and degrade trust, notify the owner, and eventually block publication or mark the entity unverified. It should not silently invent a current value.

The operational consequence is: A failure at any stage should preserve the last known valid entity while making staleness and rejection visible. Deleting a valid entity because the newest commit contains malformed YAML can make incidents worse. Conversely, serving a stale owner indefinitely without warning creates false trust. The platform needs both continuity and freshness policy.

## 10. Can one API have several implementing components?

Yes for replicas or deliberate multi-implementation contracts, but the ownership and compatibility model must explain it. An accidental count greater than one can indicate duplicate authority.

The strongest engineering interpretation is: Catalog.from records and the TypeScript Catalog perform the same checks: canonical identity, unique entities, known owners, known systems, valid relations, and at least one provider for each API. The implementation intentionally keeps catalog validation separate from contract parsing and runtime discovery.

## 11. Why build a relation graph?

It enables impact analysis: which components consume an API, which resources support a service, and which owner responds. A flat inventory cannot answer change or outage questions.

The defect-oriented view is: Now take api:default/analysis-http. Its owner is Analysis Control. Two components consume it: the graph gateway and the API platform for publication or sandbox workflows. The relation graph therefore supports an impact question: would a breaking HTTP change affect Graph API behavior or platform examples? The registry and consumer catalog add version detail to answer it.

## 12. Which catalog fact should a consumer trust most?

Trust is not a ranking of fields. The consumer needs an owner, lifecycle, released contract, environment, and support path whose sources and freshness are visible.

Across the Python and TypeScript tracks, the invariant is: Fact Authority Derived projections Reconciliation --- --- --- --- API owner API product metadata portal, support routing reject unknown group released bytes contract registry docs, SDK build, gateway config verify digest runtime route deployment control plane portal status compare desired/observed active consumer consumer registry and usage evidence deprecation report expire stale observations carefully service objective owning service scorecard require fresh evidence
