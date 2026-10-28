# Catalog, Ownership Graph, and Metadata Authority

**Module 02 of 10**

> **Governing question:** How can a central catalog be useful without pretending to own every fact it displays?

## Place in the program

Module 01 established what the platform owns. Module 02 creates the authoritative inventory needed to make those boundaries discoverable and enforceable.

## Learning outcomes

- model components, APIs, resources, systems, domains, and groups
- assign canonical identity and accountable ownership
- separate authoritative, derived, and observed metadata
- validate relations and detect orphans
- use the graph for impact and support analysis

## Capstone result

Publish the Analysis Platform catalog and ownership graph.

## Catalog versus spreadsheet

A software catalog is a graph of identified entities and relationships, not a list of service names. The capstone models domains, systems, groups, components, APIs, and resources. Each entity has a canonical reference such as `api:default/analysis-http`. Components declare provided and consumed APIs; resources remain distinct from API boundaries.

The graph answers operational questions: which component implements Analysis Events API? Which owner is responsible? Which services consume it? Which database supports the component? Those answers are prerequisites for compatibility, support, deprecation, and incident response.

## Sources of truth

Metadata should live near the source that can maintain it. A component descriptor in source control is authoritative for its owner-declared relationships. The contract registry is authoritative for released bytes and digests. The identity directory is authoritative for group membership. Runtime discovery is authoritative for current instances. The catalog assembles these facts and records provenance; it does not magically become the creator of every fact it displays.

Derived facts must be labeled. “Component A consumes API B” may be declared by A, inferred from gateway traffic, or observed from runtime telemetry. These are different evidence classes. An inferred relation can trigger review but should not overwrite owner-declared intent without a policy.

## Canonical identity

The capstone uses `kind:namespace/name`. Names are lowercase and stable. Titles may change; identity should not. Renaming an entity is a migration with aliases and consumer impact, not a cosmetic edit. Canonical references prevent `analysis-api`, `Analysis API`, and `analysis_http` from becoming three policy subjects.

## Ownership is an accountable relation

Every active component, API, resource, system, and domain points to a group entity. The group is not only an email address. It has membership, escalation, and continuity when individuals change. The platform team validates that the owner exists; the organization determines who belongs to the group.

An owner is responsible for semantics, lifecycle, operational response, and risk decisions. A “maintainer” who can merge code but cannot accept compatibility or incident responsibility is not necessarily the owner.

## Orphans, duplicates, and stale facts

The catalog proof rejects an API without an implementing component. It also rejects unknown owners, unknown relations, missing systems, and noncanonical references. A production catalog should also report stale entities, duplicate candidate identities, ownerless repositories, and runtime resources not represented in source metadata. These are inventory reconciliation problems, not merely YAML lint.

## Backstage descriptor profile

The course includes a `catalog-info.yaml` using the Backstage entity vocabulary. Backstage describes components, APIs, resources, systems, groups, and directional relations. The local core validates a bounded semantic subset so the learner can see the rules. Optional external validation can test the descriptors in a real Backstage environment. The distinction prevents the course from claiming full compatibility based on a homegrown parser.

## Worked impact query

Suppose Analysis Events API 1.0 changes. The catalog graph identifies Analysis Control as provider, Analysis API Platform and downstream projection components as consumers, and the owning group. The registry supplies the contract release. Consumer records add versions and criticality. This combined graph is what allows a deprecation decision later; no single file provides the complete answer.

## Implementation review

`Catalog.from_records` and the TypeScript `Catalog` perform the same checks: canonical identity, unique entities, known owners, known systems, valid relations, and at least one provider for each API. The implementation intentionally keeps catalog validation separate from contract parsing and runtime discovery.

## Standards anchors

Backstage’s [descriptor format](https://backstage.io/docs/features/software-catalog/descriptor-format/) defines the shape of catalog entities, while its [catalog graph](https://backstage.io/docs/features/software-catalog/creating-the-catalog-graph/) illustrates ownership, inventory, lifecycle, dependency mapping, and API exposure. Use those concepts as a model, not as permission to hide authoritative sources.


## Entity ingestion and processing

Treat catalog ingestion as a pipeline:

```text
authoritative descriptor
→ parse
→ canonicalize identity
→ validate policy
→ resolve references
→ derive relations
→ record source and freshness
→ publish searchable projection
```

A failure at any stage should preserve the last known valid entity while making
staleness and rejection visible. Deleting a valid entity because the newest
commit contains malformed YAML can make incidents worse. Conversely, serving a
stale owner indefinitely without warning creates false trust. The platform needs
both continuity and freshness policy.

Record the source location, source revision, ingestion time, processor version,
and validation result. If a processor derives a relation—such as an inverse
`ownerOf` edge—mark it as derived. If runtime telemetry suggests a consumer
relation, mark it observed. Consumers of the catalog can then decide which level
of evidence suits impact analysis.

## Relation semantics

Use directed, typed edges. Important examples include:

- component **provides** API;
- component **consumes** API;
- component **depends on** resource;
- API **belongs to** system;
- entity **owned by** group;
- system **part of** domain.

An inverse edge can be generated for navigation, but the original declaration
retains authority. Avoid generic `dependsOn` for everything. A service consuming
an API has compatibility obligations; a service using a database has operational
and data obligations. Collapsing these prevents useful policy.

## Ownership changes

Changing an owner is not a text edit. Verify that the new group exists, accepts
responsibility, has support and incident routes, and receives pending lifecycle
work. Preserve history so an incident can identify who owned the API at a given
time. If a team dissolves, the parent system or domain owner should become the
escalation owner until transfer completes; the API should not become ownerless.

For high-criticality APIs, ownership transfer should include:

- open incidents and support tickets;
- active consumers and commitments;
- pending deprecations;
- security exceptions;
- reliability objectives and runbooks;
- package and registry permissions;
- runtime deployment authority.

## Metadata freshness

Different fields age differently. Contract digest and release time are immutable.
Runtime instance count can be stale within seconds. Owner membership may be
refreshed daily. Documentation quality evidence might expire quarterly. A single
“last updated” timestamp is therefore misleading. Model freshness per source or
evidence kind.

A policy can require that an active API’s owner and support route are fresher
than 24 hours, while compatibility evidence remains valid for the immutable
release. The catalog should display the distinction rather than one green icon.

## Reconciliation loops

Compare three inventories:

1. **Declared:** source-controlled catalog entities.
2. **Published:** registry releases and package artifacts.
3. **Observed:** runtime routes, telemetry, brokers, and deployed components.

Differences generate actions:

- declared but not published may be proposed work;
- published but not declared is an ownership defect;
- observed but not published may be shadow traffic or an emergency route;
- declared active but not observed may be an outage or stale lifecycle;
- observed consumers absent from registration create deprecation uncertainty.

Automated reconciliation should report and route discrepancies. It should not
silently choose one source and mutate the others.

## Catalog query design

A useful catalog supports queries such as:

- Show active APIs owned by a group and their evidence freshness.
- Show consumers of a deprecated release by criticality.
- Show components depending on a resource involved in an incident.
- Show APIs with no current sandbox or support route.
- Show runtime routes whose digest is not the active registry release.

These are decision queries. Search by name remains useful, but it is not the
highest-value function of the catalog.

## Catalog security and privacy

Catalog metadata can expose internal topology, owners, runtime resources, and
security classifications. Apply audience views and least privilege. Public,
partner, and internal catalogs may share identity but expose different details.
Do not embed credentials or sensitive operational data in descriptors. The
platform itself needs audit records for ownership and lifecycle changes.


## Worked catalog walkthrough

Take `component:default/analysis-graph-gateway`. Its owner is the API Platform
team, its system is Analysis Platform, it provides Analysis Graph API, and it
consumes Analysis HTTP, Artifact HTTP, and Notification HTTP capabilities. This
record does not mean the platform team owns project or artifact facts. It means
the team owns the component that composes those facts under source-service
contracts.

Now take `api:default/analysis-http`. Its owner is Analysis Control. Two
components consume it: the graph gateway and the API platform for publication or
sandbox workflows. The relation graph therefore supports an impact question:
would a breaking HTTP change affect Graph API behavior or platform examples?
The registry and consumer catalog add version detail to answer it.

## Catalog change workflow

A safe metadata change follows:

```text
owner edits descriptor
→ pull-request validation
→ relation and policy preview
→ owner/reviewer approval
→ merge with source revision
→ catalog ingestion
→ derived graph update
→ affected-owner notification
```

For high-impact changes such as owner transfer or API retirement, include an
impact preview. The catalog should not make destructive graph changes merely
because a YAML field changed.

## Catalog quality dimensions

Evaluate:

- **Completeness:** expected entities and required fields exist.
- **Correctness:** authoritative owners confirm facts.
- **Freshness:** volatile facts meet source-specific age bounds.
- **Consistency:** relations agree across sources or discrepancies are visible.
- **Uniqueness:** canonical identities do not collide.
- **Coverage:** observed runtime and registry subjects are represented.
- **Usability:** users can answer decisions without private interpretation.

These dimensions should not become one average. Missing owner is a blocker;
slightly stale description text may be a review item.

## Failure investigation

When an orphan appears, do not immediately assign it to the platform team. Trace
source history, runtime deployment, registry publication, and organizational
changes. The orphan may be a retired component still running, a team rename, an
emergency route, or a genuinely abandoned service. The correct remedy depends on
which authority is wrong.

## Evidence before progression

Complete the module laboratory and checkpoint. The evidence must show the decision and its consequences; screenshots of a portal or a green status badge are not sufficient.

## Metadata authority matrix

A catalog becomes trustworthy only when each field has one authority and a
reconciliation rule. In the capstone, an API owner is declared by the API
product record and must resolve to a real group. Runtime deployment state is not
owned by the catalog; it is observed from the runtime control plane and linked
to the catalog entity. A contract version and digest come from the registry.
Consumer relationships come from explicit registration plus observed use. A
support route may be derived from the catalog owner, but an incident escalation
policy is owned by the operational governance process.

Write an authority matrix before adding metadata:

| Fact | Authority | Derived projections | Reconciliation |
|---|---|---|---|
| API owner | API product metadata | portal, support routing | reject unknown group |
| released bytes | contract registry | docs, SDK build, gateway config | verify digest |
| runtime route | deployment control plane | portal status | compare desired/observed |
| active consumer | consumer registry and usage evidence | deprecation report | expire stale observations carefully |
| service objective | owning service | scorecard | require fresh evidence |

This prevents “last writer wins” metadata. If a portal form can change a field
that a source repository also owns, one system eventually overwrites the other.
Either designate one writer or create an explicit proposal and approval flow.

## Ownership transfer

Teams change. A catalog that merely stores a group name cannot handle transfer.
A safe ownership transfer identifies the current owner, proposed owner,
contracts and consumers affected, operational duties, open exceptions, and the
effective time. Both sides acknowledge the transfer. Runtime escalation and
support routing change atomically with the authoritative owner record, while
historical release records retain the publisher and owner at publication time.

An API with a dissolved team is not “temporarily ownerless.” It is an incident
and lifecycle risk. Block new releases, route escalation to the system owner,
and establish an explicit transfer. Do not silently assign everything to the
platform team: that hides organizational debt and turns the platform into the
owner of facts it cannot safely operate.

## Topology questions the graph must answer

A useful relation graph answers practical questions:

- Which component implements this API?
- Which consumers are affected by retirement?
- Which services depend on this resource?
- Which team receives a contract-semantics ticket?
- Which interfaces become undiscoverable if this component disappears?
- Which runtime routes implement an approved release?

The graph should not infer unsupported causality. `consumesApis` means a declared
contract dependency, not proof that every request currently flows. `dependsOn`
means an operational dependency, not business ownership. Keep relation
vocabulary small, defined, and testable. Unbounded free-text relations make the
catalog visually rich and operationally weak.

In the capstone, the Analysis Graph Gateway consumes service-owned HTTP
capabilities and provides the graph API. This relation does not authorize the
gateway to own artifact or notification data. The API Platform component
consumes interface metadata for publication and discovery; that does not make it
a runtime dependency of every business request. A relation graph is useful
precisely because it preserves these distinctions.

## Implementation drill: canonical identity before relations

Relations are safe only after identifiers are canonical. Normalize the kind,
but reject names that would produce multiple spellings for one entity.

```python
import re

NAME = re.compile(r"^[a-z][a-z0-9-]{0,62}$")

def entity_ref(kind: str, namespace: str, name: str) -> str:
    normalized_kind = kind.strip().lower()
    if not NAME.fullmatch(namespace) or not NAME.fullmatch(name):
        raise ValueError("invalid-entity-name")
    if not NAME.fullmatch(normalized_kind):
        raise ValueError("invalid-entity-kind")
    return f"{normalized_kind}:{namespace}/{name}"
```

```typescript
const namePattern = /^[a-z][a-z0-9-]{0,62}$/;

function entityRef(kind: string, namespace: string, name: string): string {
  const normalizedKind = kind.trim().toLowerCase();
  if (!namePattern.test(namespace) || !namePattern.test(name)) {
    throw new Error("invalid-entity-name");
  }
  if (!namePattern.test(normalizedKind)) {
    throw new Error("invalid-entity-kind");
  }
  return `${normalizedKind}:${namespace}/${name}`;
}
```

After identity validation, catalog proof can require known owners, systems,
providers, consumers, and dependency targets. Do not “helpfully” rewrite names
inside relations; reject noncanonical input so the owner fixes the source.
