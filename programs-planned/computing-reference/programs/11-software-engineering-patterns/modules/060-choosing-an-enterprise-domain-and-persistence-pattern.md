---
module_id: SEPAT-060
program: Software Engineering: Patterns
level: 2
module_number: 60
title: Choosing an Enterprise Domain and Persistence Pattern
status: complete
last_verified: 2026-08-29
---

# Choosing an Enterprise Domain and Persistence Pattern

## One-Page Review

### Governing question

How should architects choose and evolve a coherent combination of domain-logic and persistence patterns from evidence about rule complexity, invariant scope, identity, set orientation, schema divergence, transactionality, workloads, team capability, and operational risk—without turning pattern selection into fashion or an automatic score?

### Essential definitions

- A **domain-logic pattern** assigns ownership of business rules: Transaction Script, Table Module, Active Record, or Domain Model.
- A **data-source pattern** mediates storage: gateways, Active Record, or Data Mapper, commonly supported by Unit of Work, Identity Map, and loading strategies.
- A **decision context** is one bounded business capability and its commands, queries, invariants, data ownership, quality attributes, constraints, and change history.
- **rule interaction** measures how strongly rules share concepts, state transitions, temporal premises, and invariants—not merely their count.
- **set orientation** means behavior is naturally expressed over many rows/tuples rather than one identity-centered object graph.
- **representation divergence** is the structural and lifecycle mismatch between domain concepts and persistence/API schemas.
- A **fitness function** is an observable architecture property with an evidence method and threshold, such as transaction completeness or query budget.
- A **reversibility seam** is a tested boundary that permits a pattern to be replaced locally without a system-wide rewrite.
- A **hybrid** uses different coherent patterns for different capabilities or read/write paths; it is not arbitrary mixing inside one invariant.
- **pattern debt** is the measured cost of a chosen pattern no longer matching the behavior, data, or operational shape.

### Central model, mechanism, or theorem

Let a decision context have evidence vector

\[
x=(r,s,i,d,t,q,o,h),
\]

where \(r\) is rule interaction, \(s\) set orientation, \(i\) identity/lifecycle importance, \(d\) representation divergence, \(t\) transaction breadth, \(q\) read/query asymmetry, \(o\) operational constraints, and \(h\) human/team capability. A candidate architecture \(a\) is admissible only if every hard constraint \(g_j(a,x)\) holds. Among admissible candidates, compare evidence-backed trade-offs:

\[
A(x)=\{a\mid \forall j,\ g_j(a,x)=\mathrm{true}\},
\qquad
a^*\in\operatorname{Pareto}(A(x)).
\]

There is generally no universal scalar optimum. A pattern that dominates latency in one workload may lose on correctness clarity, change isolation, or operability. Architecture selection is a falsifiable hypothesis reviewed over time.

### Critical invariants

- Choose within a named bounded capability and use case; do not prescribe one pattern for an entire enterprise by slogan.
- Separate domain-logic ownership from persistence mapping, transaction, identity, and loading choices.
- Hard correctness, security, regulatory, latency, availability, and data-ownership constraints eliminate candidates before convenience scoring.
- Model the actual invariant and change shape; table count, endpoint count, or framework popularity are not adequate proxies.
- Commands, read models, bulk work, and analytical paths may use different patterns while sharing explicit consistency boundaries.
- Transactions, authorization, idempotency, audit, constraints, and external-effect delivery have explicit owners regardless of pattern.
- Every choice records alternatives, assumptions, evidence, risks, fitness functions, and triggers for reconsideration.
- Migration proceeds through tested seams, data reconciliation, compatibility, observability, and rollback—not a flag-day rewrite.
- Teams may adopt only complexity they can operate and review, while training or tooling closes capability gaps.
- High-stakes domain validity requires named human review; pattern pedigree and green tests are insufficient.

### Common failures

Common failures include “always use Domain Model,” CRUD prejudice, ORM-driven design, one pattern for reads and writes, scoring matrices that conceal veto constraints, mistaking table count for domain complexity, anemic entities plus service god objects, rich objects for set-based jobs, Active Record callbacks for workflows, repositories that merely rename tables, premature CQRS/event sourcing, shared databases that erase ownership, mocked persistence tests, accidental distributed transactions, performance claims without representative data, team-skill fatalism, and rewrites without compatible migration evidence.

### Compact example

A small deterministic classifier receives three bounded profiles. A simple membership registry yields Transaction Script plus Active Record; set-oriented nightly fee accrual yields Table Module plus Data Mapper; interacting claim adjudication yields Domain Model plus Data Mapper. Its output is a shortlist for review, not a proof or production architecture.

### Connections

[SEPAT-059](059-lazy-load.md) completes the loading mechanics used by persistence designs; [SEPAT-061](../ROADMAP.md) begins messaging patterns. Selection connects to [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), [Database Engineering](../../18-database-engineering/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), and [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md).

## Governing Question

How can a team select the least complex enterprise domain and persistence design that makes its real invariants, changes, data access, transactions, security, and operations explicit—and know when evidence says to evolve it?

Pattern choice is not a ranking from primitive to sophisticated. Transaction Script is not an immature Domain Model; Table Module is not failed object orientation; Active Record is not automatically an anti-pattern; Data Mapper is not automatically clean architecture. Each assigns different costs and ownership.

## Why This Matters

Enterprise systems persist consequential state over years. A mismatch between behavior shape and architecture produces duplicated rules, hidden transactions, query explosions, callback workflows, mapper machinery, or object graphs that fight set-based data.

Overengineering is also risk. A rich model, repositories, events, multiple stores, and asynchronous projections can make a simple registry harder to reason about and operate. The best current design is the simplest admissible one, not the design with the most named patterns.

Selection must remain revisable. Rule interaction, load, regulation, schemas, ownership, and team knowledge change. Recording evidence and seams enables convergence without pretending the first choice is timeless.

## Prerequisites and Retrieval

You should understand Transaction Script, Table Module, Domain Model, Service Layer, Unit of Work, Identity Map, Data Mapper, Active Record, Lazy Load, relational transactions, authorization, idempotency, outbox, migrations, and representative performance testing. Retrieve these distinctions:

1. Domain-logic organization and data-source mapping are separate axes even when Active Record combines them.
2. One use case may require several records and effects; individual repository/model saves do not define its atomic boundary.
3. Complex SQL does not necessarily imply a complex domain, and a small schema can encode difficult temporal rules.
4. Read/report workloads often benefit from projections or set operations rather than mutable domain graphs.
5. A database constraint can enforce representable data integrity across every writer; an object invariant alone cannot.
6. Splitting a process/service cannot make an invariant disappear; it changes coordination and failure modes.
7. Architectural tests and metrics support stated properties but do not establish business, legal, clinical, or ethical correctness.

## Learning Objectives

After completing this module, you should be able to:

- characterize a bounded decision context using invariant, identity, set, divergence, transaction, query, operational, and team evidence;
- distinguish domain-logic patterns from data-source and behavioral support patterns;
- eliminate candidates using hard constraints before comparing trade-offs;
- match Transaction Script, Table Module, Active Record, and Domain Model to appropriate behavior shapes;
- choose gateways, Data Mapper, Unit of Work, Identity Map, loading, repositories, and projections deliberately;
- design coherent command/read/bulk hybrids and consistency boundaries;
- reject premature distribution, CQRS, and event sourcing while recognizing evidence that justifies them;
- record an architecture decision with fitness functions and reconsideration triggers;
- plan incremental extraction or simplification with compatibility, reconciliation, and rollback evidence;
- construct a high-stakes review that names required domain, security, accessibility, regulatory, data, and operations reviewers.

## Core Exposition

### Begin with a bounded decision context

Name the capability, actors, commands, decisions, queries, state, owners, upstream/downstream contracts, and prohibited outcomes. Draw transaction and consistency boundaries before classes. A “platform architecture” decision is usually too broad; enrollment, pricing, settlement, catalog search, and access review can require different patterns.

Inventory current evidence: rule changes, defects, incident paths, query/load profiles, data volume/skew, schema ownership, deployment constraints, recovery objectives, audit/regulatory requirements, and team experience. Separate known measurements from forecasts and preferences.

### Model invariants before mechanisms

Write each important invariant as scope, premises, decision, state touched, concurrency window, and enforcement evidence. Determine whether it is row-local, aggregate-local, set-wide, temporal, or cross-system. If cross-system, decide which system owns truth and how other systems tolerate delay/failure.

A domain object is useful when it creates a coherent place to decide interacting behavior. It is not useful merely because nouns can become classes. Conversely, set SQL is useful when behavior genuinely concerns a relation; forcing millions of rows through objects can obscure correctness and cost.

### Evaluate rule interaction, not rule count

Ten independent field checks can remain simple. Three rules sharing policy version, lifecycle, money, time, and several entities may demand a richer model. Look for duplicated conditionals, invalid intermediate states, changes touching many scripts, temporal history, alternate calculations, and terminology important to domain experts.

High interaction supports value objects, policies, aggregates, and a Domain Model. Low interaction supports Transaction Script or Active Record. Interaction can differ by capability.

### Choose Transaction Script for simple use-case logic

Transaction Script organizes each request/use case as a procedure. It fits straightforward orchestration, modest rules, explicit inputs/outcomes, and direct set/row persistence. Keep scripts cohesive, parameterized, authorized, idempotent where needed, and transactionally explicit.

Extract shared value calculations/policies rather than copying them. When scripts duplicate lifecycle decisions or require complex shared state, that is evidence—not a deadline slogan—to introduce richer ownership.

### Choose Table Module for set-centered behavior

Table Module has one module/object handling all rows in a table or view rather than one object per row. It fits set calculations, batches, accounting periods, ranking, allocation, and legacy record-set tooling where relational shape is primary.

Define transaction, locking/isolation, tenant/filter, constraint, affected-row, idempotency, audit, batching, and reconciliation semantics. Do not make the module a generic table API; name domain operations over sets.

### Choose Active Record for cohesive row-centered behavior

Active Record fits when one row is a natural identity/lifecycle unit, domain and schema evolve together, rules are mostly row-local, and framework convenience reduces accidental machinery. Use named domain methods, protected fields, scoped queries, constraints, versions, and an application transaction for multi-record use cases.

It strains under interacting cross-record rules, alternative representations, many persistence stores, callback workflows, or schema/domain divergence. The response is not necessarily a full rewrite: extract values/policies, operations, projections, then aggregates/mappers where pressure exists.

### Choose Domain Model for interacting concepts and rules

A Domain Model combines meaningful data and behavior across entities, value objects, policies, and aggregates. It fits interacting invariants, lifecycle, calculations, alternatives, and terminology that must remain coherent across use cases.

Keep aggregate boundaries small enough for transaction/concurrency ownership. A “rich model” does not mean a fully connected ORM graph or all logic inside entities. Application services coordinate authorization, repositories, transactions, idempotency, outbox, and external workflows; domain objects decide domain rules from explicit premises.

### Select persistence independently

Transaction Script may call a Table Data Gateway, SQL/query module, or repository. Table Module naturally works with records/tables. Active Record combines record object and persistence access. A Domain Model commonly uses Data Mapper/repositories so domain concepts remain independent of schema.

Unit of Work coordinates changes and a transaction; Identity Map maintains per-context representation; Lazy Load or explicit loaders manage acquisition. These support patterns are optional mechanisms whose semantics must be justified. Do not add all of them because a diagram says “enterprise.”

### Evaluate representation divergence

Data Mapper earns its cost when domain and storage shapes differ: aggregates span tables, values need conversion, legacy schemas use alien terminology, several read/write representations exist, or the domain must run/test without storage infrastructure. It also centralizes identity/change tracking complexity.

If schema and model align and will co-evolve, Active Record or gateways can be clearer. A repository whose methods mirror generic CRUD and return persistence-shaped records provides abstraction ceremony without semantic independence.

### Separate commands, reads, and bulk work

Commands that protect invariants may use a Domain Model or named Active Record operations. Reads can use direct projections, query services, or materialized views. Bulk reconciliation/accrual can use Table Module/set SQL. This hybrid is coherent when each path has explicit ownership and consistency.

Do not load write aggregates for dashboards merely to preserve uniformity. Do not let a read model become an unguarded write path. Track freshness, source, schema compatibility, authorization, deletion, and reconciliation for derived views.

### Put transactions around invariants

Choose transaction scope from the decision, not class boundaries. One operation may update aggregate state, request/idempotency, audit, and outbox atomically. Database constraints/guarded writes protect concurrency; locks or versions detect conflict.

If an invariant spans independently failing systems, first question ownership. Prefer one authoritative decision and asynchronous propagation. Distributed transactions, sagas, reservations, or compensations have specific semantics; none recreates arbitrary global atomicity for free.

### Treat distribution as a constraint multiplier

Process/service boundaries add network failure, retries, duplicate/reordered messages, partial deployment, schema evolution, observability, and operational ownership. They may be justified by independent scaling, isolation, regulatory boundaries, data ownership, or team autonomy—but not by pattern fashion.

Start with clear modules and ownership. A modular monolith can preserve transaction simplicity and later extraction seams. A monolith can still be poorly modular; a service mesh does not create domain boundaries.

### Require evidence before CQRS or event sourcing

CQRS can separate substantially different command and query models. Event sourcing can preserve an event history as the authoritative state transition record. Benefits may include temporal audit, alternate projections, and replay; costs include event semantics/versioning, upcasting, projection lag, privacy/deletion, operational recovery, and reasoning about time.

Use them when those properties are requirements and the team can operate them. An outbox plus ordinary state tables is not event sourcing. Separate read projections do not require separate services or stores.

### Include security and privacy in selection

Authorization must remain visible near each command/query and derive tenant, actor, action, purpose, and sensitive fields from trusted context. An identity map, repository, aggregate, or filtered query is not automatically a security boundary.

Patterns affect disclosure: lazy traversal can reveal fields, projections can minimize data, shared tables complicate tenant isolation, events preserve history, and caches extend retention. Threat model every candidate and test alternate/bulk/admin paths.

### Include operational and team constraints

Assess deployment, migrations, on-call debugging, backup/restore, reconciliation, capacity, observability, incident containment, and dependency/tool maturity. A theoretically expressive design that the team cannot inspect or recover is inadmissible until capability exists.

Do not freeze weak architecture under “the team is not ready.” Make the gap explicit and fund training, pairing, tooling, or narrower scope. Complexity should be paid for by a demonstrated property.

### Use hard constraints before a trade-off matrix

List non-negotiable properties: atomic decision boundary, maximum latency, offline behavior, privacy retention, audit immutability, deployment topology, approved technology, recovery objectives. Eliminate candidates that cannot meet them with credible evidence.

Then compare admissible candidates across clarity of invariant ownership, change locality, persistence fit, query efficiency, testability, operability, migration cost, team fluency, and reversibility. Keep uncertainty ranges and evidence links. Do not average away a catastrophic security or correctness failure with developer-convenience points.

### Prefer Pareto reasoning to fake precision

Candidate A dominates B if it is no worse on every relevant dimension and better on at least one under comparable evidence. Often several candidates remain nondominated. Choose based on contextual priorities and reversible experiments.

Weighted scores can facilitate discussion but weights and ordinal ratings are judgments. Record sensitivity: if a small weight change flips the winner, the decision is uncertain and needs stronger evidence or a reversible trial.

### Run architecture experiments

For uncertain hotspots, implement a thin vertical slice using representative rules, schema, concurrency, and data. Measure change effort, query/row/byte behavior, transaction correctness, failure recovery, mapping friction, test diagnostics, and operational visibility.

A toy CRUD benchmark cannot evaluate evolving invariants. Preserve experiment outputs under governed evidence, state limits, and avoid silently shipping a prototype whose failure modes were excluded.

### Record the decision and reconsideration triggers

An architecture decision record names context, hard constraints, alternatives, decision, evidence, consequences, risks, fitness functions, owner, review date, and triggers. Triggers might include duplicated rule defects, callback growth, aggregate contention, query budget breach, mapping churn, schema ownership change, new regulatory retention, or recovery failure.

Review on triggers, not arbitrary architecture seasons. Evidence can support keeping the current design.

### Establish fitness functions

Useful functions include: invariants mapped to one owner/enforcement path; forbidden dependency tests; transaction/concurrency scenarios; mutation tests for rules; query/row/byte budgets; no hidden loads at serialization; migration compatibility; outbox/reconciliation lag; authorization matrix; deployment/recovery drills; and bounded module coupling.

Automate where semantics are mechanically observable, then retain human review for conceptual coherence and domain policy. A green structural test cannot prove a boundary is correct.

### Evolve incrementally

From Transaction Scripts, extract shared values/policies and route selected use cases through them. From a Fat Active Record, extract explicit application operations, remote effects to outbox/workflow, query projections, then rich aggregates and Data Mapper where needed. From overbuilt Domain Models, collapse ceremony around truly simple records/use cases.

Use compatible schema changes, dual-read/write only with precise authority/reconciliation, backfill checkpoints, shadow comparisons, canaries, and rollback/forward paths. Move one invariant owner at a time and prevent old/new paths from both deciding truth.

### Evaluate high-stakes contexts separately

For finance, clinical, safety, public policy, or regulated decisions, enumerate prohibited outcomes, uncertainty, human override, audit, explainability, accessibility, privacy, retention, and incident recovery. Named domain and affected-stakeholder reviewers validate the real rule model.

Pattern choice can improve traceability and enforcement but cannot certify substantive correctness. Record unresolved premises and fail/degrade according to approved policy.

### Executable model: an auditable shortlist, not an oracle

The finite classifier applies transparent threshold rules to three profiles. It shows that logic-owner and persistence choices are separate. It neither evaluates hard constraints nor proves that the recommended shortlist is correct for a real system.

<!-- bijux-verify: {"id":"enterprise-pattern-shortlist","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"membership: logic=Transaction Script persistence=Active Record\nfee-accrual: logic=Table Module persistence=Data Mapper\nclaim: logic=Domain Model persistence=Data Mapper\n","stderr":""}} -->
```python
def shortlist(profile):
    if profile["rule_interaction"] >= 4 and profile["identity"] >= 3:
        logic = "Domain Model"
    elif profile["set_orientation"] >= 4:
        logic = "Table Module"
    elif profile["row_centered"] >= 4:
        logic = "Active Record"
    else:
        logic = "Transaction Script"

    if profile["representation_divergence"] >= 3 or logic == "Domain Model":
        persistence = "Data Mapper"
    elif logic == "Active Record" or profile["row_centered"] >= 3:
        persistence = "Active Record"
    else:
        persistence = "Table Data Gateway"
    return (logic, persistence)


profiles = [
    ("membership", {"rule_interaction": 1, "identity": 2, "set_orientation": 1,
                    "row_centered": 3, "representation_divergence": 1}),
    ("fee-accrual", {"rule_interaction": 2, "identity": 1, "set_orientation": 5,
                    "row_centered": 1, "representation_divergence": 4}),
    ("claim", {"rule_interaction": 5, "identity": 5, "set_orientation": 2,
               "row_centered": 2, "representation_divergence": 4}),
]

for name, profile in profiles:
    logic, persistence = shortlist(profile)
    print(f"{name}: logic={logic} persistence={persistence}")
```

### Finite invariant argument

Each profile contains every accessed key, so the function is total over this finite input set. Branches assign exactly one logic owner: membership reaches the final Transaction Script branch; fee-accrual reaches Table Module; claim satisfies the first Domain Model branch. Persistence is evaluated separately: membership's row-centered score selects Active Record, while fee-accrual and claim have divergence at least three and select Data Mapper.

The loop emits one line per input in stable order. No branch mutates the profiles. Thus the stated output follows for these exact mappings. Thresholds are author-supplied judgments, the categories omit constraints and hybrids, and integer ratings are not measurements. The program is an inspectable teaching model, not a selection algorithm suitable for production governance.

### Evidence classification

The snippet report empirically establishes deterministic execution and exact output for three profiles. The branch trace is independently recomputable. It provides no evidence about a real domain's rules, costs, constraints, team, architecture, security, performance, migration, or pattern fitness.

## Definitions and Notation

The evidence vector \(x=(r,s,i,d,t,q,o,h)\) uses contextual observations, not universal normalized measurements. Each component must include its source, unit/rubric, uncertainty, and review date. Ordinal values cannot legitimately be multiplied as if they were physical quantities without a defended decision method.

Let \(G=\{g_1,\ldots,g_m\}\) be hard constraints. Candidate \(a\) is **admissible** when every \(g_j(a,x)\) holds with sufficient evidence. A **trade-off dimension** \(f_k(a,x)\) evaluates an admissible candidate; direction (minimize/maximize), uncertainty, and unacceptable region are explicit.

Candidate \(a\) **dominates** \(b\) when it is at least as good on every relevant \(f_k\) and strictly better on one, under comparable evidence. The **Pareto set** contains nondominated candidates. This formalism organizes reasoning; incomplete or biased dimensions still yield a poor decision.

Let \(I\) be the set of important invariants and \(O(i)\) the unique authoritative decision owner for invariant \(i\). Migration safety requires that at each cutover point exactly one path owns new decisions, even if several paths read or compare results. Reconciliation checks representations against the authoritative history/state.

A fitness function is tuple \((p,m,\theta,w)\): property \(p\), evidence method \(m\), threshold/condition \(\theta\), and owner/reaction \(w\). A metric without an owner and decision response is observation, not governance.

## Mechanisms, Invariants, or Proof Structure

The selection mechanism is a review loop:

1. Bound capability/use cases and collect evidence.
2. State invariants and ownership/consistency/security premises.
3. Generate credible domain-logic, persistence, read, bulk, and deployment candidates.
4. Eliminate candidates violating hard constraints.
5. Compare remaining candidates across declared trade-offs and uncertainty.
6. Run representative experiments for decisive unknowns.
7. Record decision, consequences, fitness functions, and triggers.
8. Implement through seams; continuously test and review evidence.

The governing invariants are: one authoritative owner per business decision; one explicit transaction/consistency policy per invariant; trusted authorization on every path; constraints and concurrency control at the shared data boundary; effects delivered under idempotency/outbox/workflow policy; reads labeled by freshness/source; no write bypass through projections/bulk/admin paths; and migration with compatible representations, reconciliation, and rollback/forward recovery.

The decision proof is defeasible. It has the form: under evidence \(E\), constraints \(G\), and priorities \(P\), candidate \(a\) is admissible and no evidenced alternative dominates it; experiment/fitness evidence supports specified properties. Counterevidence—new rule interaction, contention, load, security boundary, ownership, or operational failure—invalidates a premise and triggers review. It does not prove the original team was irrational.

Verification triangulates architecture tests, real persistence/concurrency/fault experiments, production-like performance, migration rehearsal, threat/privacy analysis, operability drills, and conceptual/domain review. No single layer substitutes for the others.

## Alternatives and Trade-Offs

| Logic owner | Strong fit | Cost introduced | Reconsider when |
|---|---|---|---|
| Transaction Script | Simple explicit use cases | Duplication as rules interact | Shared lifecycle/rules diverge |
| Table Module | Set-oriented relational behavior | Table/schema coupling | Identity-rich interactions dominate |
| Active Record | Row-centered behavior/schema alignment | Persistence/lifecycle coupling | Cross-record rules/callbacks grow |
| Domain Model | Interacting concepts/invariants | Modeling/mapping machinery | Behavior remains trivial/ceremonial |

| Persistence/read mechanism | Strong fit | Main risk |
|---|---|---|
| Table/Row Gateway | Explicit thin SQL boundary | Business logic leaks/duplicates |
| Active Record | Direct aligned row access | Schema and domain lock together |
| Data Mapper + repository | Domain/storage independence | Mapping/identity/UoW complexity |
| Projection/query service | Purpose-built reads | Freshness and duplicated schemas |
| Table Module/set SQL | Bulk/relational operations | Bypass of lifecycle/events/versions |
| Event-sourced state | Authoritative transition history | Evolution, replay, privacy, operations |

A bounded hybrid often wins: Domain Model/Data Mapper for claim decisions, projections for search, Table Module for reconciliation, and outbox for integration. Its boundary contracts matter more than uniform naming.

## Failure Modes and Misconceptions

- **“Domain Model is the destination.”** It fits interacting behavior, not every mature system.
- **“Transaction Script is technical debt.”** Cohesive simple scripts can be the least risky design.
- **“Table Module is not object-oriented enough.”** Set-based domains should not be distorted to satisfy style.
- **“Active Record cannot contain domain behavior.”** It can own cohesive row-centered rules; problems arise when rules outgrow the row/lifecycle.
- **“Data Mapper decouples everything.”** Domain code can still depend on repository query shapes, transactions, and storage assumptions.
- **“Repository means one interface per table.”** A domain repository represents aggregate-oriented access; generic CRUD may add no semantic seam.
- **“Use one pattern consistently.”** Uniformity across unlike commands, reads, and batches can increase complexity.
- **“Scores pick the architecture.”** Ratings/weights encode judgment and cannot override hard constraints.
- **“Microservices solve tangled models.”** Distribution adds failure while tangled ownership may remain.
- **“CQRS requires two databases.”** Logical command/read separation can exist in one process/store.
- **“An outbox means event sourcing.”** It is durable integration delivery, not necessarily authoritative event history.
- **“Mocks make persistence replaceable.”** They can conceal isolation, constraints, identity, SQL, and migration coupling.
- **“Team skill decides forever.”** Capability is a constraint to address, not a permanent excuse or a reason for unoperable novelty.
- **“A rewrite is cleaner.”** Flag-day replacement loses behavioral evidence and creates two incomplete truths.
- **“Green tests prove the domain.”** They test encoded claims; named experts must validate high-stakes rules.

## Worked Examples

### Example 1

**Situation.** A small membership registry has create, rename, suspend, and list operations with row-local rules.

**Reasoning.** Transaction Scripts or named Active Record methods plus constraints/versions are sufficient. A rich aggregate/repository hierarchy would add little current value.

**Conclusion.** Choose the simplest admissible row/use-case design and record triggers such as interacting benefit rules.

### Example 2

**Situation.** Nightly fees apply a policy version to ten million eligible accounts and must reconcile totals.

**Reasoning.** The operation is set-oriented. A Table Module/set SQL with batches, snapshot/locks, idempotency, audit/outbox, affected-row checks, and reconciliation avoids hydrating objects.

**Conclusion.** Bulk domain behavior can belong to a set-centered module.

### Example 3

**Situation.** Insurance claim adjudication combines coverage version, evidence, parties, exclusions, money, lifecycle, appeals, and explainability.

**Reasoning.** Interacting concepts support Domain Model, application operation, and Data Mapper/repository. Read projections support queues/reports; workflows own external evidence and notifications.

**Conclusion.** Rich behavior and representation divergence justify richer boundaries.

### Example 4

**Situation.** A Rails content model has eight fields, two transitions, and an aligned table; policy says Active Record is forbidden.

**Reasoning.** The prohibition is stylistic, not evidence. Active Record with protected transitions, constraints, versions, scopes, and bounded callbacks may minimize cost.

**Conclusion.** Evaluate the pattern in context rather than by reputation.

### Example 5

**Situation.** A dashboard hydrates 100,000 domain objects only to sum three columns.

**Reasoning.** The read is relational/set-based and does not decide aggregate invariants. Use authorized SQL/projection/materialized view with freshness/reconciliation.

**Conclusion.** A Domain Model need not own every read.

### Example 6

**Situation.** Two services both decide whether a subscription may renew and disagree during deployment.

**Reasoning.** Distribution duplicated invariant ownership. Choose one authority; other service requests/consumes versioned outcomes and handles delay/idempotency. Reconcile historical divergence.

**Conclusion.** A boundary must assign truth, not merely data copies.

### Example 7

**Situation.** A team proposes event sourcing solely because audit is required.

**Reasoning.** Immutable audit records plus current-state tables and outbox may meet requirements with simpler deletion/recovery. Event sourcing is justified only if authoritative history/replay/temporal projections outweigh evolution and operational costs.

**Conclusion.** Requirement-to-mechanism traceability prevents pattern inflation.

### Example 8

**Situation.** A Fat Active Record performs pricing, payments, notifications, reporting, and 60 callbacks.

**Reasoning.** Characterize behavior, move effects to outbox/workflows, queries to projections, extract values/policies and explicit operations, then map rich aggregates separately. Preserve compatibility and reconcile each cutover.

**Conclusion.** Evolution follows pressures one invariant at a time.

### Example 9

**Situation.** A decision matrix scores microservices 82 and modular monolith 79.

**Reasoning.** Sensitivity shows two arbitrary weight changes reverse the result; distributed transaction and on-call capability are hard constraints excluded from score. Run a vertical slice and keep the reversible simpler boundary meanwhile.

**Conclusion.** Close scores reveal uncertainty, not mathematical truth.

### Example 10

**Situation.** A clinical dosing capability must combine medication, renal function, allergy, current guideline, clinician authority, and override.

**Reasoning.** Model explicit decision evidence and known/unavailable states in a reviewed Domain Model/application operation; use authoritative scoped repositories, guarded versions, audit/outbox, fail/degrade policy, accessible UI, and named clinical/safety/privacy review.

**Conclusion.** Pattern structure supports—but never substitutes for—high-stakes human validation.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) develops boundaries, quality attributes, decisions, modularity, and evolutionary fitness.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) grounds transactions, constraints, plans, set operations, migrations, and recovery.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies application operations, idempotency, projections, and boundary contracts.
- [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md) develops ownership, consistency, messaging, retries, and partial failure.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies threat modeling, authorization, tenant isolation, privacy, and audit.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) develops fitness functions, integration, concurrency, fault, performance, and migration evidence.
- [SEPAT-059](059-lazy-load.md) completes enterprise persistence mechanics; [SEPAT-061](../ROADMAP.md) begins messaging and integration choices.

## References

1. Martin Fowler, [“Transaction Script”](https://martinfowler.com/eaaCatalog/transactionScript.html), *Patterns of Enterprise Application Architecture* catalog, 2003.
2. Martin Fowler, [“Table Module”](https://martinfowler.com/eaaCatalog/tableModule.html), *Patterns of Enterprise Application Architecture* catalog, 2003.
3. Martin Fowler, [“Domain Model”](https://martinfowler.com/eaaCatalog/domainModel.html), *Patterns of Enterprise Application Architecture* catalog, 2003.
4. Martin Fowler, [“Data Mapper”](https://martinfowler.com/eaaCatalog/dataMapper.html), *Patterns of Enterprise Application Architecture* catalog, 2003.
5. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002. Domain logic, data source, object-relational behavior, and distribution patterns.
6. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2004. Bounded contexts, models, repositories, services, aggregates, and context boundaries.
7. Vaughn Vernon, *Implementing Domain-Driven Design*, Addison-Wesley, 2013. Strategic/tactical design and integration choices.
8. Neal Ford, Rebecca Parsons, and Patrick Kua, *Building Evolutionary Architectures*, 2nd ed., O’Reilly, 2022. Fitness functions and guided incremental change.
9. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Storage, transactions, derived data, streams, consistency, and distributed trade-offs.
10. Sam Newman, *Building Microservices*, 2nd ed., O’Reilly, 2021. Service boundaries, decomposition, data ownership, migration, and operations.

## Exercises

### Exercise 1

Create an evidence vector, hard constraints, candidate set, and fitness functions for a tenant-scoped appointment scheduling capability. Compare at least three logic/persistence combinations without using a single aggregate score.

### Exercise 2

Choose patterns for three paths in one billing capability: interactive invoice correction, invoice search/reporting, and nightly interest accrual. Define transaction, consistency, authorization, audit/outbox, and shared ownership.

### Exercise 3

Diagnose a system with anemic entities, 90 application services, generic repositories per table, and duplicated lifecycle conditionals. Propose incremental changes and evidence gates without assuming Domain Model is the answer everywhere.

### Exercise 4

Evaluate a proposal for microservices, CQRS, and event sourcing for a growing monolith. State evidence that would justify each choice, hard disqualifiers, a reversible experiment, and migration/recovery requirements.

### Exercise 5

Design and review the domain/persistence architecture for high-stakes clinical dosing. Cover evidence states, invariant/transaction owner, representation, reads, integrations, authorization/privacy, accessibility/override, operations, verification, migration, and named human review.

## Answers to the Exercises

### Answer 1

Context: clinicians/patients create, reschedule, cancel, and search appointments across resources. Evidence vector records moderate lifecycle interaction, high identity, some set scheduling/search, domain/schema divergence, transaction across appointment/resource hold/idempotency/audit/outbox, query-heavy calendars, strict privacy/availability, and team/database capabilities. Hard constraints include tenant/patient authorization, no double-booked exclusive resource under concurrency, bounded booking latency, auditable override/cancellation, and recoverable notifications.

Candidates: (A) Transaction Script + guarded SQL/gateway, (B) named Active Records + application transaction, (C) Domain Model for Appointment/Slot policy + Data Mapper, with projections for all. Reject any candidate lacking a database-enforced exclusion/guard or equivalent serializable protocol. Compare change locality for recurrence/resource policies, query/set fit, mapping cost, real concurrency evidence, operability, and migration. Fitness functions coordinate double-booking races, authorization matrix, mutation tests for lifecycle, calendar query/row/latency budget, rollback/outbox faults, and recovery drill. If rules remain modest A/B may be nondominated; interacting recurrence/resource/override rules may support C. No scalar score is needed.

### Answer 2

Interactive correction protects invoice lifecycle, money/tax values, versions, actor authority, reason, audit, and outbox; use a Domain Model or cohesive Active Record operation according to rule interaction, behind one application transaction and guarded database constraints. Search/reporting uses tenant/field-authorized immutable projections/materialized views with explicit freshness and reconciliation; it never writes invoice truth. Nightly interest is set-oriented Table Module/SQL, partitioned and idempotent by policy/period/account, with snapshot/locks, affected-row/amount reconciliation, audit, and outbox.

One billing capability owns policy vocabulary and authoritative invoice/charge state. Projection and batch code share versioned policy definitions or independently recomputed test vectors rather than duplicating ad hoc formulas. Every path has action authorization and tenant predicates. Outbox delivers external facts; derived views acknowledge lag. Integration/property tests compare interactive and batch calculations at boundaries, and no read/bulk path bypasses guarded lifecycle/version/audit rules.

### Answer 3

Map lifecycle decisions and their duplicates by use case, record/table, policy, transaction, defects, and change frequency. Generic repositories may remain temporarily as access seams but should not be relabeled domain abstractions. Add characterization, mutation, real database concurrency, query, authorization, and rollback tests; make operation transaction/idempotency/outbox ownership explicit.

Extract duplicated pure values/policies and route one lifecycle through a named operation. Where behavior is row-local, move it into cohesive Active Record/entity or keep a clear script. Where set-based, create Table Module/query operation. Where rules strongly interact across a stable aggregate, introduce domain objects and repository/Data Mapper for that capability only. Replace table-generic repository methods with use-case/aggregate queries or direct infrastructure gateways; move reports to projections. Gate each cutover on parity/shadow comparison, constraints, version races, query budgets, telemetry, reconciliation, and rollback, then delete the old decision path so ownership remains unique.

### Answer 4

Microservices require evidence of independently owned capability/data, scaling/isolation/regulatory/deployment need, and teams able to operate network failure, schemas, observability, security, and recovery. CQRS requires materially different command/query models or loads; it need not imply another service/store. Event sourcing requires authoritative transition history, temporal/replay value, and a workable event evolution, projection, privacy/deletion, snapshot, and disaster-recovery model. Hard disqualifiers include an invariant needing unavailable cross-service atomicity, no ownership/on-call, prohibited indefinite event retention, or inability to restore/reconcile.

First impose modular boundaries and ownership in the monolith, add outbox and read projection only where evidenced, and build a vertical slice for one low-coupling capability. Inject duplicate/reordered/delayed messages, run old/new schema deployments, rebuild projections, restore backups, test authorization, and measure latency/operations. Shadow/compare while the monolith remains authoritative; cut over one decision owner with compatibility and reconciliation. Maintain rollback/forward routing, retained source history, runbooks, telemetry, and a trigger-based decision record. Do not bundle all three mechanisms into one irreversible migration.

### Answer 5

The application operation owns a single dosing decision using authenticated clinician/patient/purpose, medication/order, renal/hepatic values with provenance/time, allergies, contraindications, guideline/policy version, units, and current patient context. Evidence types distinguish present, verified absent, stale, unavailable, conflicting, and overridden. A reviewed Domain Model may express interacting dose rules and lifecycle; scoped repositories/Data Mapper isolate authoritative clinical schemas, while projections supply read-only explanation/history. One transaction/version protocol stores decision, evidence digest, authority, override reason, immutable audit, idempotency, and outbox; integrations fetch/notify through explicit deadline/retry/reconciliation workflows.

Fail or degrade only under approved clinical policy. The accessible UI presents units, source/freshness, conflicts, uncertainty, explanation, and override/escalation with keyboard/screen-reader/color-independent behavior. Enforce least privilege, field/purpose authorization, tenant/patient boundaries, privacy-minimized logs/events, retention and break-glass audit. Operations monitor freshness, disagreement, override, effect lag, rollback, and recovery without patient identifiers in metrics.

Verify pure rules with independent clinical test vectors, dimensional/boundary/property/mutation tests; real repository/database constraints, versions and races; authorization/privacy matrices; source outage/cancellation/late result; transaction/outbox/duplicate delivery; projection rebuild; migration shadow comparison/reconciliation; load, accessibility, backup/restore, and incident drills. Named pharmacists, prescribing clinicians, clinical safety/informatics, patients or representatives, privacy/legal/regulatory, security, accessibility/human-factors, data/database, SRE, and incident-response owners review real policies and evidence. No pattern or automated suite alone establishes safe dosing.
