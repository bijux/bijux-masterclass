# Worked answers — Catalog, Ownership Graph, and Metadata Authority

## 1. What makes catalog metadata authoritative?

Authority comes from a declared source and owner, not from being displayed centrally. The catalog should ingest owner-maintained descriptors, validate them, record freshness, and expose derived relations without pretending that its cached copy created the fact.

## 2. Why is owner a relation rather than a free-text email?

A stable group entity supports membership, escalation, history, and machine checks. Free-text contact data becomes stale and cannot reliably connect ownership across components, APIs, and resources.

## 3. What is an orphan API?

An API with no accountable owner or no implementing component. It may have a contract file, but nobody is responsible for semantics, operation, change, or retirement.

## 4. Why must entity identity be canonical?

Canonical kind, namespace, and name prevent duplicate aliases and ambiguous references. Without canonical identity, ownership, dependency, and policy evidence can attach to different records that appear to describe the same thing.

## 5. Should the catalog own the contract bytes?

The registry owns published immutable artifacts. The catalog references the active release and owner. Combining inventory and artifact storage can work technically, but their authorities and lifecycle rules remain distinct.

## 6. What is the danger of inferred ownership?

Inference from repository names or commit history can seed a review, but silently treating it as authoritative can assign responsibility to the wrong team. Ownership needs explicit confirmation.

## 7. How are dependencies different from API consumption?

A component may depend on a database or object store without consuming an API. API consumption is a contract relationship; resource dependency is an operational relationship. Both matter but imply different ownership and change risks.

## 8. Why track lifecycle in the catalog?

Discovery must distinguish proposed experiments from active supported interfaces and deprecated or retired ones. Without lifecycle, consumers can adopt unsupported or dying APIs.

## 9. What should happen to stale metadata?

The platform should expose freshness and degrade trust, notify the owner, and eventually block publication or mark the entity unverified. It should not silently invent a current value.

## 10. Can one API have several implementing components?

Yes for replicas or deliberate multi-implementation contracts, but the ownership and compatibility model must explain it. An accidental count greater than one can indicate duplicate authority.

## 11. Why build a relation graph?

It enables impact analysis: which components consume an API, which resources support a service, and which owner responds. A flat inventory cannot answer change or outage questions.

## 12. Which catalog fact should a consumer trust most?

Trust is not a ranking of fields. The consumer needs an owner, lifecycle, released contract, environment, and support path whose sources and freshness are visible.
