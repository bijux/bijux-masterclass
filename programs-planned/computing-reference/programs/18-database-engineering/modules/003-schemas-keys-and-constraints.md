---
module_id: DBE-003
program: Database Engineering
level: 1
module_number: 3
title: Schemas, Keys, and Constraints
status: complete
last_verified: 2026-08-30
---

# Schemas, Keys, and Constraints

## One-Page Review

### Governing question

How can a database schema make legal states explicit, identify facts stably, and reject invalid transitions at the boundary shared by every writer?

### Essential definitions

A **schema** names relations, attributes, domains, and integrity rules. A **database state** is legal when every declared constraint holds. A **superkey** uniquely identifies tuples; a **candidate key** is a minimal superkey. One candidate key may be designated the **primary key** and the others are alternate keys. A **foreign key** requires each non-null referencing value tuple to match an eligible key in the referenced relation. Domain, `NOT NULL`, `CHECK`, uniqueness, key, and referential constraints restrict progressively wider parts of the state.

### Central model, mechanism, or theorem

Treat every constraint as a predicate over a proposed database state. A transaction may move state `D` to `D'` only if all constraints required at its checking point are true in `D'`. Keys establish identity through values; foreign keys establish existence relationships; checks encode row-local propositions. Immediate and deferred checking change when rejection occurs, not which committed states are legal.

### Critical invariants

- Attribute values conform to declared domains, precision, collation, and nullability.
- Every candidate key is unique and irreducible; primary-key components are non-null.
- A foreign key targets a declared eligible key with matching arity and compatible comparison semantics.
- Referential actions preserve the intended ownership and lifecycle semantics.
- Defaults generate values but do not excuse any constraint violation.
- Constraint names and failure behavior are stable enough to diagnose and operate.
- Indexes may implement constraints, but a performance structure is not automatically a semantic declaration.
- Every write path, including imports, repairs, replication, and migrations, preserves or explicitly audits invariants.

### Common failures

Common failures include using mutable business attributes as identifiers without migration design, declaring surrogate keys while omitting real-world uniqueness, treating `UNIQUE` as portable null semantics, assuming `CHECK (x > 0)` rejects null, reversing foreign-key direction, cascading across independent lifecycles, omitting indexes needed to operate referential actions, relying only on application validation, disabling enforcement without reconciliation, and adding constraints to dirty data without validating the existing population.

### Compact example

`Customer(customer_id, email)` uses `customer_id` as its primary key and `email` as an alternate candidate key. `Order(order_id, customer_id, amount)` has its own primary key, a foreign key to `Customer`, and `amount > 0` plus `NOT NULL`. The order `(20, 7, 40)` is legal only if customer 7 exists. A default order ID cannot rescue a missing customer, and a unique customer ID cannot prevent two rows from sharing an email unless that business rule is also declared.

### Connections

[DBE-002](002-relational-model-and-relational-algebra.md) defines relation schemas and set semantics. [DBE-004](../ROADMAP.md) derives redundancy and normalization from functional dependencies. SQL querying, transactions, indexing, recovery, replication, and online schema change later explain how constraints are evaluated, implemented, preserved, and evolved.

## Governing Question

A relation schema says which tuples can be discussed; an integrity schema says which collections of tuples may coexist. The engineering question is not merely how to spell `CREATE TABLE`. It is how to translate facts such as “an invoice has one identity,” “an order names an existing customer,” and “an interval ends after it begins” into rules that remain true under every authorized writer and failure-recovery path.

The relational model separates logical facts from storage. That freedom depends on a precise contract. Without keys, a tuple cannot be referenced unambiguously. Without domains and checks, semantically impossible values can enter. Without referential constraints, relationships can point to absent facts. Without migration and validation discipline, a declaration can describe intended data while old or bypassed rows violate it.

The answer is to model constraints as predicates over states and transitions. The database owns the final shared enforcement boundary. Applications may provide earlier, friendlier validation, but concurrent services, imports, administrative sessions, and future clients cannot safely share application-only assumptions.

## Why This Matters

Integrity errors compound. A duplicate customer may split payments and support history; an orphan line item may disappear from joins; an invalid currency or negative quantity may propagate through reports. Downstream code then accumulates reconciliation logic for states that should never have committed.

Constraints also document semantics in executable form. A named unique constraint communicates an identity rule to humans, query planners, migration tools, and error handlers. A foreign key exposes a dependency graph. A check captures a proposition close to the data it governs. Catalog inspection can reveal these rules without reverse-engineering every application.

Enforcement has operational consequences. Uniqueness usually needs an index-like access path. Deleting a referenced row may inspect many referencing rows. Adding a constraint may scan existing data and hold locks. Deferred constraints retain pending obligations until commit. The schema is therefore both a semantic contract and part of the workload.

There are limits. Many rules depend on other rows, time, external systems, authorization, or a sequence of events. A row-local `CHECK` cannot express “account balance equals the sum of all posted entries” portably. A foreign key cannot prove that a customer is entitled to view an order. Constraints are strongest when each rule is placed at the narrowest authoritative layer able to observe and serialize the relevant state.

## Prerequisites and Retrieval

Retrieve sets, predicates, functions, tuples, relations, logical implication, and minimality. From [DBE-002](002-relational-model-and-relational-algebra.md), recall that a mathematical relation has no duplicate tuples, while SQL tables normally use bag-like behavior and null markers.

You should distinguish a database state from a transaction that proposes a new state. Basic SQL data-definition syntax is helpful, but this chapter derives the semantics independently of a particular engine. Null and three-valued logic receive a dedicated treatment in DBE-018; here their effects are stated wherever they alter integrity.

## Learning Objectives

After completing this module, you should be able to:

1. define schemas and constraints as predicates over database states;
2. distinguish superkeys, candidate keys, primary keys, alternate keys, natural keys, and surrogate keys;
3. prove whether an attribute set is a candidate key from stated dependencies;
4. design composite primary and foreign keys with compatible semantics;
5. explain domain, nullability, uniqueness, check, and referential constraints;
6. reason about nulls in `UNIQUE`, `CHECK`, and foreign-key rules;
7. select referential actions from ownership and lifecycle requirements;
8. distinguish immediate from deferred checking and `NO ACTION` from `RESTRICT`;
9. separate semantic declarations from indexes and application validation;
10. plan constraint introduction, validation, observation, and rollback for existing data.

## Core Exposition

A **schema** is a durable logical contract. For relation `R`, it names attributes, domains, defaults or generation rules, and constraints. A database schema also names relationships and assertions spanning relations. Its legal-state set can be written `Legal(S) = {D | every constraint in S is true on D}`. This view prevents a common category error: a constraint is not a cleanup query or a user-interface hint; it defines membership in the set of allowed states.

A **domain** supplies the admissible representation and comparison operations for an attribute: integer, fixed-precision decimal, date, text under a collation, an enumerated state, or a user-defined domain. Width is not meaning. A text field that happens to contain ISO currency codes is not constrained to that code set. Choose types that preserve required precision and comparison semantics, then add narrower constraints where the type is broader than the business domain.

Nullability is independent. SQL's null marker means missing or inapplicable information rather than an ordinary domain value. `NOT NULL` excludes it. Optionality should be semantic, not a convenience for incomplete ingestion. If a fact is temporarily unknown, model its lifecycle deliberately; if it cannot exist for a valid entity, require it.

A **default** supplies a value when a write omits one. It is not a constraint. The generated value must still satisfy type, nullability, uniqueness, foreign-key, and check rules. Defaults are evaluated according to engine semantics, often per inserted row. A default such as the current timestamp records database evaluation time, not necessarily event time.

Let `K` be a subset of attributes of relation schema `R`. `K` is a **superkey** when no two distinct tuples in any legal instance agree on all attributes in `K`. It is a **candidate key** when it is a superkey and no proper subset of `K` is a superkey. Minimal means set inclusion, not the fewest bytes or columns among all candidates.

Designating one candidate key as the **primary key** is a convention for the principal row identity and default reference target. The remaining candidates are **alternate keys** and deserve unique declarations if the corresponding rules are real. A primary key neither creates the other candidate keys nor makes every non-key attribute unique.

A **natural key** consists of values meaningful outside the database, such as `(country_code, tax_number)` under a jurisdictional rule. A **surrogate key** is introduced mainly for database identity, such as a sequence value or UUID. This is not an either-or choice. A surrogate may provide compact, stable references while a natural alternate key prevents duplicate real-world facts. Surrogates hide key width and mutability from children; they do not eliminate business identity.

Key selection requires explicit scope and time. An email address is usually mutable and may be recycled; it is not automatically a person key. A serial number may be unique only per manufacturer. A tenant-local sequence requires `(tenant_id, local_id)` to be globally distinguishing. Every claim should state its universe, comparison/collation, null policy, and historical reuse rule.

SQL **unique constraints** enforce a declared uniqueness rule, but null treatment varies by feature and product. PostgreSQL's ordinary unique constraints allow multiple nulls by default because nulls are not considered equal, and PostgreSQL also supports `NULLS NOT DISTINCT`. Portable designs make null expectations explicit and test the selected engine. A primary key normally combines uniqueness with non-nullability.

A **check constraint** is a predicate evaluated for each relevant row. `CHECK (amount > 0)` rejects false, but in SQL it generally accepts unknown; a null amount makes the comparison unknown. Use `amount NOT NULL` as well when absence is illegal. Checks are best for deterministic propositions over the row. Product-specific functions, mutable external lookups, or other-table reads can make restore and revalidation disagree with the original write.

A **foreign key** from referencing relation `C` attributes `F` to referenced relation `P` attributes `K` requires every applicable `F` value tuple to equal some `K` value tuple. `K` must be an eligible unique key. Arity, ordering, types, coercions, and collations matter. For composite keys, partial nulls can create surprising exemptions under default matching; `MATCH FULL` or component `NOT NULL` rules may better represent all-or-none relationships.

Foreign-key direction follows existence dependence: the child/referencing table stores values naming the parent/referenced table. This does not necessarily imply object ownership. An order line is often owned by an order; an order's reference to a product does not imply that deleting the product should delete historical lines.

Referential actions are transition policies:

- `NO ACTION` rejects a violation at the constraint's checking point and may permit a deferred transaction to repair an intermediate state.
- `RESTRICT` rejects the referenced change without permitting deferral of that action.
- `CASCADE` propagates deletion or key update to referencing rows.
- `SET NULL` removes an optional reference if nullability permits it.
- `SET DEFAULT` substitutes a declared default only if the resulting reference is legal.

Select these actions from aggregate ownership, audit retention, and legal lifecycle—not convenience. Cascades can be correct for contained components and disastrous across independent records. Mutable referenced keys expand update and locking costs; stable keys ordinarily avoid update cascades.

**Immediate** checking rejects as soon as the engine-defined statement boundary is reached. A **deferrable** constraint can postpone checking until transaction commit, allowing temporarily inconsistent ordering such as swapping two unique positions or loading a cyclic graph. Deferral does not permit an invalid committed state. It enlarges the set of legal intermediate states and shifts failures later, so transaction owners must handle commit-time rejection.

Constraints and indexes overlap but are not identical. An engine may implement primary and unique constraints using unique indexes. A bare unique index may not carry identical portability, deferral, null, catalog, or foreign-key eligibility semantics. Foreign-key enforcement also needs to find matching referenced rows and, for parent deletion/update, matching child rows. The referenced key is indexed by its uniqueness mechanism; the referencing columns often need a separate index for predictable operational cost.

Constraint ownership extends beyond ordinary writes. Bulk loaders, repair scripts, logical replication, restore procedures, partition operations, and online migrations may validate at different times or bypass a normal application. If enforcement is disabled or declared not enforced, the system owes a reconciliation process and must prevent unsupported completion claims.

Introducing a constraint into an existing table has two obligations: prevent new violations and prove the existing population is clean. Some engines support separating installation from validation, reducing the lock duration of the initial change. Operators must still measure validation scans, observe lock/wait/replication effects, identify offending keys, and retain a rollback or forward-repair plan. A constraint that has not validated historical rows is evidence about future enforcement only.

## Definitions and Notation

Let database state `D` map every relation schema to a finite relation instance. A constraint `c` denotes a predicate `c(D)`.

- `D` is **legal** under schema `S` exactly when `C_S(D) = AND_{c in S} c(D)` is true.
- A transition `D -> D'` may commit only when `C_S(D')` is true for every enforced committing constraint.
- Projection `pi_K(r)` retains attributes in `K`.
- `K` is a superkey of `R` when `t1[K] = t2[K]` implies `t1 = t2` for every pair in every legal instance of `R`.
- `K` is a candidate key when it is a superkey and every proper subset of `K` is not a superkey.
- `FK_{C.F -> P.K}(D)` holds when each applicable `f in pi_F(C)` has some `p in P` with `f = p[K]`, subject to the declared null matching rule.
- A constraint is **state-local** when it depends only on the proposed row, **relation-local** when it quantifies one relation, and **database-local** when it relates several relations.

Under SQL semantics, true, false, and unknown must be distinguished. A check commonly rejects only false, so unknown passes. Key and foreign-key specifications define their own treatment of null rather than inheriting ordinary equality naively.

## Mechanisms, Invariants, or Proof Structure

Derive a schema through five obligations.

First, state facts in domain language and define their grain: what does one tuple assert? Second, identify all candidate keys with scope, time, and comparison assumptions. Third, declare attribute and tuple predicates. Fourth, map relationships with cardinality, optionality, ownership, and lifecycle actions. Fifth, design enforcement, validation, observation, and migration for every writer.

To prove a candidate key, show uniqueness from the domain assumptions, then show minimality by constructing or permitting a legal counterexample for every proper subset. To disprove a proposed key, one legal pair of distinct tuples agreeing on it suffices. Observed uniqueness in a sample is empirical evidence, not a universal rule.

For foreign keys, check referenced uniqueness, compatible comparison, null policy, and transition closure. Analyze insert/update/delete on both sides. A design is incomplete if it proves inserts safe but ignores parent deletion, key changes, or bulk repair.

The bounded model below treats constraints as independent named predicates. A transition copies the state, applies one proposed insert, validates the entire candidate state, and commits only when no violation remains. It demonstrates duplicate primary-key, orphan-reference, and positive-amount rejection plus atomic preservation of the prior state.

<!-- bijux-verify: {"id":"finite-integrity-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid_errors=()\nduplicate_key=('customer.primary_key',)\norphan_order=('order.customer_foreign_key',)\nbad_amount=('order.amount_positive',)\natomic_reject=True\nstate_unchanged=True\n","stderr":""}} -->
```python
def validate(state):
    customers = state["customers"]
    orders = state["orders"]
    errors = []

    customer_ids = [row["customer_id"] for row in customers]
    if None in customer_ids or len(customer_ids) != len(set(customer_ids)):
        errors.append("customer.primary_key")

    emails = [row["email"] for row in customers if row["email"] is not None]
    if len(emails) != len(set(emails)):
        errors.append("customer.email_alternate_key")

    order_ids = [row["order_id"] for row in orders]
    if None in order_ids or len(order_ids) != len(set(order_ids)):
        errors.append("order.primary_key")

    if any(row["customer_id"] not in set(customer_ids) for row in orders):
        errors.append("order.customer_foreign_key")

    if any(row["amount"] is None or row["amount"] <= 0 for row in orders):
        errors.append("order.amount_positive")

    return tuple(errors)


def proposed_order(state, row):
    candidate = {
        "customers": [dict(item) for item in state["customers"]],
        "orders": [dict(item) for item in state["orders"]] + [dict(row)],
    }
    errors = validate(candidate)
    return (state if errors else candidate), errors


valid = {
    "customers": [
        {"customer_id": 7, "email": "ada@example.test"},
        {"customer_id": 8, "email": None},
    ],
    "orders": [{"order_id": 20, "customer_id": 7, "amount": 40}],
}
duplicate = {
    "customers": valid["customers"] + [
        {"customer_id": 7, "email": "other@example.test"}
    ],
    "orders": valid["orders"],
}
orphan = {
    "customers": valid["customers"],
    "orders": [{"order_id": 21, "customer_id": 99, "amount": 10}],
}
bad_amount = {
    "customers": valid["customers"],
    "orders": [{"order_id": 22, "customer_id": 7, "amount": 0}],
}
before = valid["orders"]
after, rejected = proposed_order(
    valid, {"order_id": 23, "customer_id": 404, "amount": 5}
)

print(f"valid_errors={validate(valid)}")
print(f"duplicate_key={validate(duplicate)}")
print(f"orphan_order={validate(orphan)}")
print(f"bad_amount={validate(bad_amount)}")
print(f"atomic_reject={bool(rejected)}")
print(f"state_unchanged={after['orders'] == before}")
```

The dictionary oracle is simple but not independent of every mechanism: `set(customer_ids)` supports both uniqueness and referential lookup. The model omits SQL null variants, collation, concurrency, deferral, cascades, indexes, storage, and crash recovery. Its evidence is deliberately bounded to the named finite states and atomic transition function.

## Alternatives and Trade-Offs

**Natural versus surrogate identity:** Natural keys prevent duplicate domain facts directly and improve interoperability, but can be wide, mutable, sensitive, or jurisdiction-scoped. Surrogates stabilize references and can improve locality, but require alternate constraints to preserve business uniqueness. A common robust design uses both.

**Sequence versus UUID:** Central sequences are compact and index-friendly but expose approximate insertion order and require allocation coordination. UUIDs can be generated across nodes, but version choice affects locality, metadata exposure, collision assumptions, and security. RFC 9562 defines current UUID layouts; a UUID still needs a database uniqueness declaration when collision is unacceptable.

**Constraint versus application validation:** Application validation gives contextual messages and can check external services, but it races with other writers and can be bypassed. Database constraints serialize shared invariants. Use both when they serve different purposes; never claim the earlier check replaces authoritative enforcement.

**Immediate versus deferred:** Immediate rejection localizes errors and limits invalid intermediate states. Deferral enables cyclic insertion, key swaps, and batch transformations, at the cost of later failures and larger pending work. Choose per invariant and transaction pattern.

**Restrict versus cascade:** Restriction forces explicit lifecycle orchestration and protects independent records. Cascades encode ownership and reduce partial cleanup for true aggregates. Deep or cyclic cascades enlarge lock scope and blast radius.

**Strict schema versus flexible payload:** Typed columns and constraints make important facts queryable and enforceable. Semi-structured payloads ease evolution for sparse, volatile, or externally owned attributes. A durable boundary often extracts identity, tenancy, lifecycle, and query-critical facts into constrained columns while validating payload versions separately.

**Synchronous versus asynchronous cross-boundary integrity:** A single database can enforce a foreign key transactionally. Independent services or regions may accept asynchronous validation and compensation to preserve autonomy or availability. That is a weaker temporal guarantee and must be named, monitored, and reconciled rather than described as an enforced foreign key.

## Failure Modes and Misconceptions

1. Inferring keys from currently distinct sample values rather than domain rules.
2. Adding a surrogate primary key and forgetting the natural alternate key.
3. Choosing mutable email, phone, or display names as stable identity without an update plan.
4. Omitting tenant scope from supposedly unique local identifiers.
5. Assuming `UNIQUE` treats null identically across products and options.
6. Assuming `CHECK (x > 0)` also means `x NOT NULL`.
7. Using floating-point types for exact monetary constraints.
8. Letting collation make two business identifiers compare unexpectedly equal or distinct.
9. Reversing parent and child in a foreign-key declaration.
10. Referencing a non-unique parent attribute.
11. Misordering components of a composite foreign key.
12. Allowing partially null composite references unintentionally.
13. Treating `NO ACTION` and `RESTRICT` as universally identical.
14. Cascading deletion from an independent reference into historical facts.
15. Believing a foreign key automatically creates every operationally necessary child index.
16. Treating a unique index as universally interchangeable with a declared unique constraint.
17. Using volatile or external-state functions inside checks.
18. Enforcing only in one application while imports and repair tools bypass it.
19. Installing an unvalidated constraint and claiming all historical data is legal.
20. Disabling constraints for a load without a quarantine and reconciliation proof.
21. Ignoring commit-time failures from deferred constraints.
22. Changing types, collations, or key generation without testing dependent references.
23. Replicating child rows before parents and mistaking transient apply failures for corrupt source data.
24. Treating database integrity as authorization, provenance, authenticity, or semantic truth.

## Worked Examples

### Example 1

**Situation:** `Enrollment(student_id, course_id, term, grade)` permits one grade per student/course/term. Is `(student_id, course_id)` a key? **Reasoning:** A student may take the same course in different terms, so two legal tuples can agree on that pair and differ in `term`. Adding `term` makes the tuple unique under the stated rule. Removing any of the three permits a counterexample. **Conclusion:** `(student_id, course_id, term)` is a candidate key; the two-column pair is not.

### Example 2

**Situation:** `User` has surrogate `user_id` but signup must not create two accounts for the same normalized login within a tenant. **Reasoning:** `user_id` distinguishes already-created rows but says nothing about domain duplication. Declare primary key `user_id` and alternate uniqueness on `(tenant_id, normalized_login)`, with explicit collation/normalization. **Conclusion:** Surrogate identity and business uniqueness are separate constraints.

### Example 3

**Situation:** A nullable `nickname` has `UNIQUE`. Can the design assume at most one missing nickname? **Reasoning:** Ordinary SQL uniqueness commonly treats nulls as distinct, and product options differ. The intended rule might allow many missing values, require at most one, or require non-null. **Conclusion:** State null semantics explicitly and use engine-supported syntax or a different model; do not infer them from the word `UNIQUE`.

### Example 4

**Situation:** `Payment(amount CHECK (amount > 0))` accepts a row whose amount is null. **Reasoning:** `NULL > 0` evaluates to unknown, and a SQL check normally rejects false rather than unknown. Add `amount NOT NULL` when absence is illegal. **Conclusion:** Range and nullability constraints solve different obligations.

### Example 5

**Situation:** `OrderLine(order_id, line_no)` is referenced by `ShipmentLine(order_id, line_no)`. **Reasoning:** The parent key and child foreign key must both contain two components in the same semantic order. Referencing only `line_no` is invalid because line numbers repeat across orders. **Conclusion:** Composite identity must propagate intact unless a separate globally unique key is introduced.

### Example 6

**Situation:** Deleting an `Order` should delete its `OrderLine` rows but must preserve a `Product` referenced by those lines. **Reasoning:** Lines are owned components of the order, so cascading from order to lines matches lifecycle. Products are independent catalog facts, so deletion should be restricted or retired explicitly. **Conclusion:** Referential actions encode domain ownership, not merely graph reachability.

### Example 7

**Situation:** Two rows with unique positions 1 and 2 must swap positions. **Reasoning:** Immediate uniqueness rejects the first update because the other row still occupies the target. A transaction with a deferrable unique constraint can create a temporary duplicate, complete the swap, and validate uniqueness at commit. **Conclusion:** Deferral changes permitted intermediate states, not the committed invariant.

### Example 8

**Situation:** Adding a foreign key to 500 million existing rows causes a long validation scan. **Reasoning:** First detect and quarantine orphans, estimate scan and lock cost, install future-write enforcement using an engine's safe unvalidated mode if available, then validate separately while observing replication and latency. **Conclusion:** Declaration and historical proof may be staged, but completion requires both.

### Example 9

**Situation:** Parent deletion is slow although the parent key is indexed. **Reasoning:** The engine can locate the parent efficiently, but it must also find every child referencing the old key to reject or execute an action. Without a suitable child-side index, this can scan the child relation. **Conclusion:** Semantic correctness and operational access paths must both be reviewed.

### Example 10

**Situation:** Orders and customers live in separate autonomous services, so no cross-database foreign key exists. **Reasoning:** The order service can validate against a customer snapshot, accept an event reference, record provenance, monitor unresolved IDs, and compensate or quarantine. Concurrent deletion still creates a window the local check cannot close. **Conclusion:** Call this asynchronously reconciled referential integrity, state its lag/failure policy, and do not claim transactional enforcement.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) explains the trees and hashes that often implement key lookups and uniqueness.
- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects schemas to aggregates, repositories, contracts, and migration compatibility.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) must preserve identifiers and constraints across ingestion, transformations, backfills, and schema evolution.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains why constraints spanning independent partitions or services require coordination or weaker guarantees.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) separates integrity constraints from authorization, tamper evidence, provenance, and adversarial validation.
- Later DBE modules connect constraints to normalization, catalogs, transaction isolation, index maintenance, recovery, replication, and online upgrades.

## References

1. E. F. Codd, [“A Relational Model of Data for Large Shared Data Banks”](https://research.ibm.com/publications/a-relational-model-of-data-for-large-shared-data-banks), *Communications of the ACM* 13(6), 1970. IBM's author-affiliated archive of the primary relational-model foundation for keys, domains, and integrity independence.
2. PostgreSQL Global Development Group, [PostgreSQL 18: SQL Conformance](https://www.postgresql.org/docs/18/features.html), official documentation, checked 2026-08-30. A current feature-by-feature map from an implementation to ISO/IEC 9075 SQL requirements and extensions.
3. PostgreSQL Global Development Group, [PostgreSQL 18: Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html), official documentation, checked 2026-08-30. Current check, not-null, unique, primary-key, foreign-key, null, and exclusion behavior.
4. PostgreSQL Global Development Group, [PostgreSQL 18: `CREATE TABLE`](https://www.postgresql.org/docs/18/sql-createtable.html), official reference, checked 2026-08-30. Constraint timing, referential actions, matching, enforcement, and product-specific extensions.
5. PostgreSQL Global Development Group, [PostgreSQL 18: `ALTER TABLE`](https://www.postgresql.org/docs/18/sql-altertable.html), official reference, checked 2026-08-30. Adding and validating constraints on existing relations.
6. SQLite Project, [Foreign Key Support](https://www.sqlite.org/foreignkeys.html), official documentation, checked 2026-08-30. Composite keys, enforcement enablement, indexes, actions, deferral, and implementation limits.
7. K. Davis, B. Peabody, and P. Leach, [RFC 9562: Universally Unique IDentifiers](https://www.rfc-editor.org/rfc/rfc9562.html), IETF Standards Track, May 2024. Current UUID formats, versions, uniqueness scope, and database considerations.

## Exercises

### Exercise 1

For `RoomBooking(building, room, starts_at, ends_at, organizer)`, assume a room can have many bookings but no two bookings may begin at the same instant in that room. Identify a candidate key and state a separate row-local check.

### Exercise 2

`Membership(tenant_id, user_id, role)` references `User(tenant_id, user_id)`. Explain why a foreign key on `user_id` alone is insufficient, and list the parent and child declarations required by the stated scope.

### Exercise 3

A table declares `discount numeric CHECK (discount >= 0 AND discount <= 1)` but unexpectedly contains null discounts. Diagnose the behavior and propose two different valid policies.

### Exercise 4

Compare natural key `(country_code, tax_number)` with surrogate `organization_id` for an organization table used by many children. Produce a design that handles stability, domain duplication, and jurisdictional scope.

### Exercise 5

A service must accept shipments before the asynchronously replicated customer record reaches its local database. Design a truthful integrity policy, including state representation, monitoring, reconciliation, and the guarantee it must not claim.

## Answers to the Exercises

### Answer 1

Under the stated rule, `(building, room, starts_at)` is a candidate key: it distinguishes starts within a scoped room, and removing any component permits collisions across buildings, rooms, or start times. Declare `CHECK (ends_at > starts_at)` and make both timestamps non-null if incomplete intervals are illegal. The key does not prevent overlapping intervals with different start times; that needs a stronger temporal/exclusion rule or serialized procedure.

### Answer 2

`user_id` is only tenant-local, so two parents in different tenants may share it. The parent must declare `PRIMARY KEY (tenant_id, user_id)` or an equivalent eligible unique key. The child declares both components non-null when membership cannot be detached and uses `FOREIGN KEY (tenant_id, user_id) REFERENCES User(tenant_id, user_id)`. Column order, types, and comparison semantics must align. This also prevents a membership in one tenant from naming a user in another.

### Answer 3

Each comparison with null is unknown; the conjunction is unknown, and a check normally rejects only false. Policy one: require a known discount with `discount NOT NULL` plus the range check. Policy two: allow unknown discounts deliberately, document null as “not yet assigned,” and ensure consumers handle it; an explicit predicate such as `discount IS NULL OR (...)` makes intent visible. A default of zero is a third design only if “no discount” truly equals a known zero.

### Answer 4

Use `organization_id` as a stable compact primary key for child references and declare alternate uniqueness on `(country_code, tax_number)` after specifying normalization, collation, null, reuse, and history rules. If an organization can possess multiple jurisdictional registrations, move them to `OrganizationRegistration(organization_id, country_code, tax_number)` with candidate keys for registration identity and for the business uniqueness rule. The surrogate prevents update propagation; the alternate constraint prevents duplicate organizations/registrations.

### Answer 5

Represent a shipment reference as `pending`, `verified`, or `rejected`, recording customer ID, source event/version, and first-seen time. Accept only within a declared pending policy, retry against a monotonic customer feed, quarantine unresolved/contradictory references after an SLO, alert on pending age/count, and make downstream release conditional on verification. Handle later customer deletion through tombstones and domain policy. The system may claim bounded asynchronous reconciliation under measured feed assumptions; it must not claim an immediate transactional foreign key or absence of temporary orphans.
