---
module_id: DBE-002
program: Database Engineering
level: 1
module_number: 2
title: Relational Model and Relational Algebra
status: complete
last_verified: 2026-08-29
---

# Relational Model and Relational Algebra

## One-Page Review

### Governing question

How does the relational model represent facts independently of storage, and how does relational algebra compose precise queries over those facts?

### Essential definitions

- A **domain** is a set of admissible atomic values for an attribute.
- A **relation schema** names a relation and its attributes with their domains.
- A **tuple** maps every attribute in a schema to one value from its domain.
- A **relation instance** is a finite set of tuples conforming to one schema.
- **Degree** is the number of attributes; **cardinality** is the number of tuples.
- **Relational algebra** is a closed collection of operators mapping relations to relations.
- **Selection** filters tuples; **projection** keeps attributes; **rename** changes names.
- **Join** combines compatible tuples; **division** expresses “for every” conditions.

### Central model, mechanism, or theorem

A database state assigns a finite relation to each relation schema. Algebraic expressions form query trees whose leaves are input relations and whose internal nodes are operators. Closure means every result is itself a relation, so expressions compose. Query equivalence is extensional: expressions `E1` and `E2` are equivalent under stated assumptions when they produce the same relation for every legal database instance.

### Critical invariants

- Every tuple has exactly the schema's attributes and domain-correct values.
- Tuple identity comes from attribute values, not row position or storage address.
- A mathematical relation contains no duplicate tuples and has no intrinsic tuple order.
- Union, intersection, and difference require union-compatible schemas.
- Product and join must resolve colliding attribute names explicitly.
- Projection under set semantics eliminates duplicate result tuples.
- Rewrites preserve both values and schema under their declared semantic assumptions.
- SQL bag, null, and ordering behavior must not be silently substituted for pure relational algebra.

### Common failures

Common errors are calling any table-shaped file a relation, assuming row or column order is logical, confusing selection with projection, forgetting duplicate elimination after projection, joining only because columns share a name, using set identities under bag semantics without checking multiplicities, treating null as an ordinary value, and claiming two query plans are equivalent from a few test datasets.

### Compact example

Let `Enrollment(student, course)` contain `(Ada, DB)`, `(Ada, PL)`, and `(Lin, DB)`. Selection `sigma_course=DB` returns two tuples. Projection `pi_student` then returns `{Ada, Lin}`. Projecting students before selecting loses `course` and makes the predicate ill-formed. Algebra exposes both meaning and legal operator order.

### Connections

[DBE-001](001-database-systems-workloads-and-guarantees.md) places the data model inside a database-system contract. [DBE-003](../ROADMAP.md) develops schemas, keys, and constraints. [Theory of Computation](../../15-theory-of-computation-and-complexity/ROADMAP.md) supplies logic and expressiveness; later query-processing modules turn algebra trees into physical plans.

## Governing Question

A database engine stores records in pages, indexes them with trees or hashes, and moves them through memory. Those mechanisms should not determine how users state ordinary questions. The relational model supplies a logical representation of facts, while relational algebra supplies a small set of operators for deriving new facts. The central engineering achievement is data independence: queries describe relationships among values without naming pointer chains or physical access paths.

E. F. Codd's primary 1970 paper, [*A Relational Model of Data for Large Shared Data Banks*](https://doi.org/10.1145/362384.362685), argued that users and most application programs should be insulated from changes in internal representation. A relation-based model achieves that goal only when its terms are used precisely. A stored SQL table resembles a relation, but duplicates, null markers, generated identity, collation, and implementation extensions can change its semantics.

The governing question therefore has two parts: what mathematical object represents a database fact, and which transformations preserve a query's intended meaning? Answering both gives a language for schema design, query correctness, optimization, authorization, testing, and cross-system translation.

## Why This Matters

The relational model reduces accidental coupling. If an application asks for customers joined with qualifying orders, the engine may use a nested-loop, hash, or merge join; scan a table or index; push a filter down; or evaluate pieces in parallel. The logical result can remain the same. Physical freedom is possible because the query denotes a relation rather than an access procedure.

Algebra makes correctness compositional. A complex query can be decomposed into selection, projection, renaming, joining, grouping extensions, and set combination. Each node has a schema and meaning. Reviewers can ask whether a predicate is applied before an attribute disappears, whether a join has the intended condition, or whether a set difference expresses negation safely. Tests can compare an optimized expression with a simple reference expression.

Optimization itself depends on equivalence laws. Moving a selection below a join can shrink intermediate results. Combining selections can reduce operator count. Reordering inner joins can expose a cheaper plan. These rewrites are valid only under specific conditions—attribute availability, predicate purity, set or bag semantics, null treatment, and join kind. An algebraic law used outside its assumptions is a correctness bug disguised as an optimization.

The model also clarifies integrity. A relation is not a spreadsheet whose row number carries identity. Keys and constraints establish which facts may coexist; those are developed in [DBE-003](../ROADMAP.md). This chapter establishes the more basic invariant: each relation instance is a typed set of tuples and each query operator returns another well-formed relation.

Finally, algebra helps separate relational theory from SQL practice. SQL normally preserves duplicates in `SELECT ALL` behavior, includes null and three-valued logic, supports ordering only when requested, and offers aggregates and windows beyond the classical algebra. PostgreSQL 18's current [`SELECT` documentation](https://www.postgresql.org/docs/18/sql-select.html), checked 2026-08-29, explicitly states that plain `SELECT ALL` retains duplicates while `SELECT DISTINCT` removes them. Translating a theorem from set algebra into SQL requires accounting for these differences.

## Prerequisites and Retrieval

You should understand sets, Cartesian products, predicates, functions, logical conjunction and existential quantification, and the distinction between logical and physical representation. Recall that a set has no duplicates or order, and that two sets are equal when they have the same members.

You should also be able to read small Python programs. SQL familiarity is helpful but not required. In this chapter, SQL is a practical comparison point rather than the definition of the relational model.

## Learning Objectives

After completing this module, you should be able to:

- define domains, schemas, tuples, relation instances, degree, and cardinality;
- distinguish relations from physical tables, files, and ordered query results;
- derive selection, projection, rename, product, set, join, semijoin, and division results;
- infer the output schema of an algebra expression;
- translate a natural-language query into a compositional algebra tree;
- use equivalence laws with their side conditions;
- explain relational closure and its value for query composition;
- distinguish classical set semantics from SQL bag and null semantics;
- test an algebra implementation against independent finite examples;
- identify where high-consequence queries require domain-specific human review.

## Core Exposition

A **domain** `D` is a set of admissible atomic values, such as integer identifiers, ISO date values, or finite text values under a stated comparison. A named-attribute schema can be written `R(A1:D1, ..., An:Dn)`. A tuple `t` over that schema is a function mapping each attribute `Ai` to a value in `Di`. Writing tuples as functions makes attribute order irrelevant: `t[A]` selects by name.

A relation instance `r(R)` is a finite subset of the Cartesian product of its attribute domains, interpreted through the schema's names. Because it is a set, the same tuple cannot occur twice. The degree is `n`; the cardinality is `|r|`. An empty relation has cardinality zero but still has a schema. A zero-degree relation is also meaningful in formal treatments: it can encode truth or falsity by containing the single empty tuple or no tuple.

“Atomic” is relative to the chosen model. A timestamp may have internal fields, yet be treated as one domain value for a relation. The important rule is that relational operators compare and carry domain values through declared semantics; they do not navigate hidden subrecords as storage links. Nested and object-relational models deliberately extend this boundary.

Attributes have names, and tuples are unordered mappings from names to values. Presentations display columns and rows in some order for humans, but that display is not the logical relation. Without an explicit ordering operator outside classical algebra, “first row” is meaningless. Physical record identifiers are not logical tuple identity unless promoted into the schema as values.

The basic operators are:

- **Selection** `sigma_p(r)` contains each tuple `t in r` for which predicate `p(t)` is true. Its schema is unchanged.
- **Projection** `pi_L(r)` restricts every tuple to attribute list/set `L` and eliminates duplicate restricted tuples under set semantics. Its schema is `L`.
- **Rename** `rho_{B <- A}(r)` changes an attribute name, or `rho_S(r)` changes the relation name, while preserving values.
- **Union** `r union s`, **intersection** `r intersect s`, and **difference** `r - s` combine union-compatible relations.
- **Cartesian product** `r times s` contains every concatenation of one tuple from each input, provided attribute names are disjoint or renamed.

Selection is horizontal in a tabular drawing: it chooses tuples. Projection is vertical: it chooses attributes. These spatial mnemonics help, but their formal definitions matter more. Projection can reduce cardinality because different input tuples may become identical after removed attributes are forgotten.

Union compatibility ordinarily requires corresponding attribute names and domains to agree. Some positional textbook definitions permit matching by position; named relational algebra makes renaming explicit and avoids accidental alignment. Difference is directional: `r - s` contains tuples in `r` that are absent from `s`.

A **theta join** combines product and selection: `r join_p s = sigma_p(r times s)`. An **equijoin** uses equality conditions. A **natural join** equates every same-named attribute and emits one copy of each shared attribute. Natural join is concise when common names deliberately mean the same domain fact; it is dangerous when coincidental names such as `status` refer to different concepts.

An **outer join** preserves otherwise unmatched tuples using null padding, so it is an extension rather than an operator of classical two-valued set algebra. A **semijoin** `r semijoin s` returns only the attributes of `r` for tuples that match some tuple in `s`. An **antijoin** returns those with no match. Both are useful for existence and nonexistence queries and for distributed planning.

Division expresses universal conditions. If `r(X, Y)` and `s(Y)`, then `r divide s` contains each `X` value associated in `r` with every `Y` tuple in `s`. For example, “students who passed every required course” divides `Passed(student, course)` by `Required(course)`. If `Required` is empty, every candidate `student` present in `pi_student(Passed)` qualifies under the usual finite algebra definition; deciding the intended candidate universe is a schema/query-design issue.

Relational algebra is closed: each operator consumes relations and produces a relation with a determinable schema. Closure permits nesting without switching representational systems. It also creates algebra trees. Leaves are base relations; internal nodes are operators; the root is the result. A database optimizer transforms this logical tree into equivalent forms and then chooses physical algorithms.

The classical algebra and domain/tuple relational calculi have equivalent expressive power under appropriate safety restrictions, a result commonly associated with Codd's theorem. Algebra is procedural in the limited mathematical sense that an expression specifies operator composition; calculus describes predicates satisfied by result tuples. Neither specifies disk access order. Safety or domain independence prevents expressions from demanding infinite complements over values not present in the finite database or explicit constants.

Schema inference is part of query typing. For `Customer(cid, name)` and `Order(oid, cid, total)`, natural join has schema `(cid, name, oid, total)`. Projecting `name` then yields `(name)`. A selection on `total` must occur before a projection that removes `total` unless the expression is reorganized to retain it. Rename permits self-joins: two copies of `Employee(eid, manager)` need distinct attribute names before they can represent employee and manager roles.

Logical design does not prescribe physical organization. A relation may be stored as a heap file, clustered index, columnar fragments, compressed vectors, or distributed partitions. Operators may stream, materialize, spill, vectorize, or parallelize. The relational result is a semantic contract; cost and resource behavior belong to physical algebra and execution planning developed later in the program.

## Definitions and Notation

Let `R(A1:D1, ..., An:Dn)` be a relation schema and `r` a relation instance over it.

- `attrs(r)` is the set of attribute names.
- `t[A]` is tuple `t`'s value for attribute `A`.
- `|r|` is cardinality; `degree(r) = |attrs(r)|`.
- `sigma_p(r) = {t in r | p(t)}`.
- `pi_L(r) = {t restricted to L | t in r}`.
- `r times s = {t union u | t in r and u in s}` for disjoint schemas.
- `r join_p s = sigma_p(r times s)`.
- `r natural_join s` equates identically named shared attributes and merges matching tuples.
- `r semijoin s = pi_attrs(r)(r natural_join s)` under the natural-match convention.

An expression is **well typed** when every referenced attribute exists, predicates use domain-valid operations, set operands are union-compatible, and merged schemas have no unresolved collisions. An expression's **denotation** on database instance `I` is written `[[E]]_I`.

Expressions `E1` and `E2` are equivalent over legal instances `L` when `for every I in L, [[E1]]_I = [[E2]]_I`, including equal output schemas. Testing equality on selected instances can refute equivalence but cannot establish this universal claim.

## Mechanisms, Invariants, or Proof Structure

The evaluation discipline is:

1. infer every leaf schema;
2. verify the operator's input compatibility;
3. derive the output schema;
4. compute tuples according to set semantics;
5. eliminate duplicates where set construction requires it;
6. compare the result with the natural-language predicate;
7. record any departure for bags, nulls, collation, ordering, or nondeterminism.

Useful equivalences include:

- `sigma_p(sigma_q(r)) = sigma_{p and q}(r)`;
- selections commute: `sigma_p(sigma_q(r)) = sigma_q(sigma_p(r))`;
- `pi_L(pi_M(r)) = pi_L(r)` when `L subseteq M`;
- selection distributes over union: `sigma_p(r union s) = sigma_p(r) union sigma_p(s)`;
- joins are commutative and associative under compatible inner-join conditions and appropriate schema naming;
- a selection referencing only `r` attributes can move below `r join s`.

Each law has side conditions. Projection does not generally commute with selection if it removes attributes needed by the predicate. Difference is not commutative. Outer joins are not freely associative. Volatile predicates and errors can make SQL evaluation observably different even where pure algebra treats predicates as mathematical functions.

The executable model represents a relation as a schema tuple plus a set of value tuples. It implements schema-checked selection, duplicate-eliminating projection, and natural join. The example asks for names of customers having an order of at least 100. A second route constructs the same answer by joining first and filtering afterward.

<!-- bijux-verify: {"id":"finite-relational-algebra","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"qualified=(('Ada',), ('Lin',))\nequivalent=True\nprojected_customers=((1,), (2,))\n","stderr":""}} -->
```python
class Relation:
    def __init__(self, schema, rows):
        if len(schema) != len(set(schema)):
            raise ValueError("attribute names must be unique")
        width = len(schema)
        normalized = {tuple(row) for row in rows}
        if any(len(row) != width for row in normalized):
            raise ValueError("row width differs from schema")
        self.schema = tuple(schema)
        self.rows = frozenset(normalized)

    def select(self, predicate):
        indexes = {name: i for i, name in enumerate(self.schema)}
        return Relation(
            self.schema,
            (row for row in self.rows if predicate(row, indexes)),
        )

    def project(self, attributes):
        positions = [self.schema.index(name) for name in attributes]
        return Relation(
            tuple(attributes),
            (tuple(row[i] for i in positions) for row in self.rows),
        )

    def natural_join(self, other):
        shared = [name for name in self.schema if name in other.schema]
        right_only = [name for name in other.schema if name not in shared]
        left_positions = [self.schema.index(name) for name in shared]
        right_positions = [other.schema.index(name) for name in shared]
        append_positions = [other.schema.index(name) for name in right_only]
        rows = []
        for left in self.rows:
            left_key = tuple(left[i] for i in left_positions)
            for right in other.rows:
                right_key = tuple(right[i] for i in right_positions)
                if left_key == right_key:
                    rows.append(left + tuple(right[i] for i in append_positions))
        return Relation(self.schema + tuple(right_only), rows)

    def ordered_rows(self):
        return tuple(sorted(self.rows))


customers = Relation(
    ("customer_id", "name"),
    [(1, "Ada"), (2, "Lin"), (3, "Mira")],
)
orders = Relation(
    ("order_id", "customer_id", "total"),
    [(10, 1, 125), (11, 1, 40), (12, 2, 100), (13, 2, 100)],
)

large = orders.select(
    lambda row, index: row[index["total"]] >= 100
)
qualified = customers.natural_join(large).project(("name",))
join_first = customers.natural_join(orders)
second_route = join_first.select(
    lambda row, index: row[index["total"]] >= 100
).project(("name",))

print(f"qualified={qualified.ordered_rows()}")
print(f"equivalent={qualified.rows == second_route.rows}")
print(f"projected_customers={orders.project(('customer_id',)).ordered_rows()}")
```

The two equal-total orders for customer 2 demonstrate projection's duplicate elimination: `customer_id=2` appears once in the projected relation. Execution provides evidence for these finite inputs, not a universal proof of the rewrite. The implementation assumes hashable values, Python equality, no null marker, deterministic pure predicates, and schemas small enough for simple scans. It does not model domains, bags, collation, SQL errors, query optimization, concurrency, or storage.

To prove the selection-pushdown instance generally, take an arbitrary output tuple. It belongs to `sigma_p(r join s)` exactly when it is formed from matching `r` and `s` tuples and `p` holds. If `p` references only the `r` tuple, this is exactly the condition that the `r` tuple belongs to `sigma_p(r)` before the join. The two inclusions establish equality. This proof fails if `p` needs `s`, or if the join/logic semantics introduce unmatched null-padded tuples.

## Alternatives and Trade-Offs

**Named versus positional attributes.** Named algebra makes schema alignment and self-join roles explicit. Positional presentations make tuple products compact but can hide accidental column swaps. Production query systems use names plus internal identifiers to resolve ambiguity.

**Set versus bag semantics.** Sets simplify laws and match the classical model. Bags retain multiplicity, avoiding automatic duplicate elimination and supporting aggregates naturally. SQL defaults to bags for query results. Some set laws lift to bags; others require multiplicity-aware formulations. Always state the semantic regime.

**Natural versus explicit joins.** Natural join is concise and robust when shared names intentionally denote the same fact. It can silently change meaning when a new same-named column is added. Explicit conditions make intent and compatibility reviewable, at the cost of verbosity.

**Algebra versus calculus.** Algebra is convenient for operator trees and optimization. Relational calculus is convenient for declarative predicates and logical reasoning. Their core expressive equivalence does not make every concrete language feature interchangeable.

**Null markers versus explicit modeling.** SQL null supports incomplete information but introduces three-valued logic and special comparison rules. Separate relations, option-like domains, or explicit status attributes can make absence categories clearer but add joins and schema complexity. Pure relational algebra here assumes ordinary values and two-valued predicates.

**Normalized facts versus nested aggregates.** Flat relations promote compositional operations and independence. Nested or document values can align with aggregate ownership and retrieval. Extensions need explicit operators and equality semantics; they should not be called classical first-normal-form relations without qualification.

**Logical versus physical algebra.** Logical join says which tuples combine; physical hash join says how. Keeping them separate permits cost-based choice. Physical properties such as ordering or partitioning can be tracked as annotations without becoming logical tuple meaning.

## Failure Modes and Misconceptions

1. **A relation is a table display.** A display has row and column order; a mathematical relation is a schema plus an unordered tuple set.
2. **Every stored row is distinct automatically.** SQL tables can contain duplicate value rows unless constraints prevent them; pure relation instances cannot.
3. **Projection is just formatting.** It changes the schema and may reduce cardinality under set semantics.
4. **Selection chooses columns.** Selection filters tuples by a predicate; projection selects attributes.
5. **Natural join is always safest.** Coincidental same-named attributes can add unintended equality conditions.
6. **Join means foreign-key lookup.** Algebraic joins combine by predicates regardless of declared keys; keys affect integrity and cardinality reasoning.
7. **Difference means SQL `NOT IN`.** Null and three-valued logic can make SQL negation behave differently; `NOT EXISTS` and set operators also have precise semantics.
8. **Equivalent outputs on fixtures prove equivalence.** Fixtures can expose counterexamples but cannot quantify over all legal instances.
9. **Inner-join reorder laws apply to outer joins.** Null padding and unmatched-row preservation invalidate many such rewrites.
10. **No `ORDER BY` still has a stable logical order.** Any observed order is plan-dependent unless the language contract explicitly orders the result.

## Worked Examples

### Example 1

**Question:** Is `{(1, "Ada"), (1, "Ada")}` a relation instance under set semantics?

**Reasoning:** Set notation collapses identical members. The instance contains one tuple and has cardinality one. A bag can give that tuple multiplicity two, but that is a different semantic object.

**Conclusion:** Duplicate copies have no identity in a classical relation.

### Example 2

**Question:** Project `Enrollment(student, course) = {(Ada, DB), (Ada, PL), (Lin, DB)}` onto `student`.

**Reasoning:** Restriction produces `(Ada)` twice and `(Lin)` once before set construction. Duplicate elimination leaves `{(Ada), (Lin)}`.

**Conclusion:** Projection may reduce cardinality by forgetting distinguishing attributes.

### Example 3

**Question:** May `Student(id, name)` union `Course(id, name)` be evaluated because their attribute names and primitive domains match?

**Reasoning:** It is type-compatible syntactically but likely meaningless semantically: student identifiers and course identifiers belong to distinct conceptual domains. Strong domain naming or deliberate renaming exposes the mismatch.

**Conclusion:** Mechanical union compatibility is necessary but semantic compatibility is also required.

### Example 4

**Question:** Compute a natural join between `Employee(eid, dept)` and `Department(dept, building)`.

**Reasoning:** Match tuples with equal `dept` and emit `(eid, dept, building)`. Employees with no matching department disappear in an inner natural join; departments with no employees also contribute no tuple.

**Conclusion:** Natural join combines matching facts and does not preserve unmatched inputs.

### Example 5

**Question:** How do you express employees who manage another employee using a self-join?

**Reasoning:** Rename one copy to `E(eid, manager)` and another to `M(manager_id, manager_manager)`, then join on `E.manager = M.manager_id` and project the needed manager attributes. Without rename, role-specific references are ambiguous.

**Conclusion:** Rename is essential when one relation participates in multiple logical roles.

### Example 6

**Question:** Does `sigma_p(pi_L(r)) = pi_L(sigma_p(r))` always hold?

**Reasoning:** No. The left side is ill-formed if `p` references an attribute excluded from `L`. Even when it is well formed, one must check whether duplicate and predicate semantics preserve equality. If every attribute in `p` belongs to `L` under pure set semantics, the rewrite is valid.

**Conclusion:** Algebraic rewrites need attribute and semantic side conditions.

### Example 7

**Question:** What does `Passed(student, course) divide Required(course)` return?

**Reasoning:** For each candidate student appearing in `Passed`, require that every course tuple in `Required` pairs with that student in `Passed`. Extra passed courses do not disqualify a student.

**Conclusion:** Division represents universal coverage, not exact set equality.

### Example 8

**Question:** Why can SQL `SELECT customer_id FROM orders` differ from `pi_customer_id(Orders)`?

**Reasoning:** Plain SQL `SELECT` retains duplicate result rows, while relational projection constructs a set. `SELECT DISTINCT customer_id` more closely matches set projection, subject to SQL's null and comparison rules.

**Conclusion:** Similar syntax and algebra symbols do not guarantee identical multiplicity semantics.

### Example 9

**Question:** A hospital query selects patients eligible for a medication by joining diagnoses, labs, allergies, and current prescriptions. Is algebraic type checking sufficient for deployment?

**Reasoning:** No. Attribute meanings, units, time windows, missing-data policy, code-set versions, contraindication logic, and duplicate episode semantics require named clinical and data-domain review. Query equivalence, fixture tests, independent reference evaluation, lineage checks, and monitored shadow results are needed, but no result should claim clinical safety without the applicable human approval. This chapter supplies no external review.

**Conclusion:** Formally valid algebra cannot establish the domain truth or safety of a high-consequence query.

### Example 10

**Question:** Can a selection be pushed below an inner join?

**Reasoning:** If the predicate uses only left-side attributes, `sigma_p(r join s) = sigma_p(r) join s` under pure deterministic inner-join semantics. Pushing it reduces left input without changing matching tuples. With an outer join or null-sensitive predicate, construct a counterexample before applying the law.

**Conclusion:** Pushdown is both a semantic theorem with conditions and a physical optimization opportunity.

## Cross-Program Connections

Relational algebra applies finite-set and logical reasoning developed further in [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) and compositional semantics from [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md). Query typing resembles expression typing: each operator requires input schemas and derives an output schema.

[Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) implements logical operators with scans, hashing, sorting, and indexes. The same join denotation can have radically different time, space, and I/O costs. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies the physical structures while preserving logical independence.

[Data Engineering](../../19-data-engineering/ROADMAP.md) uses relational transformations in pipelines, but adds time, incremental change, lineage, and delivery semantics. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) motivates semijoins, partitioning, and the cost of moving intermediate relations. Security uses relational views and predicates to restrict observations, yet policy correctness depends on domain meaning and side channels beyond algebra.

## References

- E. F. Codd, [*A Relational Model of Data for Large Shared Data Banks*](https://doi.org/10.1145/362384.362685), *Communications of the ACM* 13(6), 377–387, 1970. Primary introduction of the relational model and its data-independence motivation.
- E. F. Codd, [*Relational Completeness of Data Base Sublanguages*](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf), in *Data Base Systems*, Courant Computer Science Symposia 6, 1972. Primary source for relational completeness and comparison with calculus.
- Serge Abiteboul, Richard Hull, and Victor Vianu, [*Foundations of Databases*](https://webdam.inria.fr/Alice/), Addison-Wesley, 1995. Author-hosted formal treatment of relational models, algebra, calculus, dependencies, and query languages.
- Hector Garcia-Molina, Jeffrey D. Ullman, and Jennifer Widom, [*Database Systems: The Complete Book*, second edition](https://cs.stanford.edu/people/widom/dbcourse.html), Pearson, 2008. Durable database foundations and relational algebra treatment.
- Raghu Ramakrishnan and Johannes Gehrke, [*Database Management Systems*, third edition](https://pages.cs.wisc.edu/~dbbook/), McGraw-Hill, 2003. Author-maintained resources for relational algebra and database implementation.
- PostgreSQL Global Development Group, [*`SELECT`, PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/sql-select.html), checked 2026-08-29. Official current set/bag, duplicate, set-operation, and ordering behavior.
- PostgreSQL Global Development Group, [*Logical Operators, PostgreSQL 18.6 Documentation*](https://www.postgresql.org/docs/18/functions-logical.html), checked 2026-08-29. Official current statement of SQL three-valued logical behavior.

## Exercises

### Exercise 1

For `Book(isbn, title, publisher)`, define schema, tuple, degree, cardinality, and the result schema of `pi_publisher(Book)`. Explain whether result order is defined.

### Exercise 2

Given `Enrollment(student, course) = {(Ada, DB), (Ada, PL), (Lin, DB)}` and `Required(course) = {(DB), (PL)}`, compute selection of DB enrollments, projection of enrolled students, natural join with `Required`, and division `Enrollment divide Required`.

### Exercise 3

Diagnose the expression “project `name` from `Customer`, then join with `Order` on `customer_id`.” Repair it and state the output schema for names of customers with orders totaling at least 100.

### Exercise 4

Compare classical relational projection with SQL `SELECT` and `SELECT DISTINCT` under duplicates, nulls, and ordering. State what must be true before translating an algebraic rewrite into SQL.

### Exercise 5

A financial sanctions process joins customer identity, aliases, jurisdictions, and time-versioned sanctions lists. Specify a relational expression strategy, adversarial cases, equivalence evidence, and named human-review roles needed before replacing an existing screening query.

## Answers to the Exercises

### Answer 1

The schema is `Book(isbn:D_isbn, title:D_text, publisher:D_publisher)` with domains chosen by the design. A tuple is a function assigning one conforming value to each of `isbn`, `title`, and `publisher`. Degree is three; cardinality is the number of distinct tuples in the current instance. `pi_publisher(Book)` has schema `(publisher:D_publisher)` and contains each represented publisher value once under set semantics. Neither the base relation nor projected result has logical tuple order; a presentation or SQL query needs an explicit ordering operation to promise one.

### Answer 2

`sigma_course=DB(Enrollment) = {(Ada, DB), (Lin, DB)}`. `pi_student(Enrollment) = {(Ada), (Lin)}` because Ada's two restricted tuples collapse. Natural join with `Required` returns all three enrollment tuples because both DB and PL are required and every enrollment course matches one required tuple. Division returns `{(Ada)}`: Ada has both required courses, while Lin lacks PL. Extra courses would not prevent qualification.

### Answer 3

The initial projection removes `customer_id`, so the proposed join predicate cannot be typed. First select qualifying orders, join on customer identifier, then project name: `pi_name(Customer join_{Customer.customer_id = Order.customer_id} sigma_total>=100(Order))`. With explicit names, the join schema includes customer attributes and order attributes, with the duplicate join key merged or separately named according to the chosen join. Final schema is `(name)`. Under set semantics, customers with multiple qualifying orders appear once.

### Answer 4

Classical projection returns a set and therefore removes duplicate projected tuples; it assumes ordinary domain values and no intrinsic order. SQL `SELECT` defaults to retaining duplicates, while `SELECT DISTINCT` removes duplicate rows using SQL comparison rules. SQL null participates in three-valued predicates and has special distinctness behavior; `ORDER BY` is required for a promised sequence. Before translating a rewrite, identify set versus bag multiplicities, nullability and truth tables, collation/equality, volatile or error-producing expressions, join kind, and ordering/limit dependencies. Then prove the law for those semantics or compare against an independently specified oracle and adversarial counterexamples.

### Answer 5

Normalize each input's identity and effective-time semantics explicitly, select list versions valid at the screening instant, rename roles, join on reviewed exact and alias keys, and project a result that preserves match evidence rather than only a Boolean. Test duplicate aliases, homonyms, transliteration, missing identifiers, conflicting dates, jurisdiction changes, retroactive corrections, empty lists, nulls, clock boundaries, and list-version rollback. Establish equivalence with a simple reference evaluator over generated and historical cases, compare matched and unmatched populations, review query plans only after semantics, and shadow the candidate with monitored discrepancies and rollback. Named reviewers must include sanctions/legal policy authority, identity/data-quality authority, database/query engineering, security/privacy, model or matching owners if approximate logic exists, and independent compliance validation required by the jurisdiction. No internal algebra test or this answer constitutes legal approval or external human review.
