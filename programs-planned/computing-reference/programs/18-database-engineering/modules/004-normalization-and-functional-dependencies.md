---
module_id: DBE-004
program: Database Engineering
level: 1
module_number: 4
title: Normalization and Functional Dependencies
status: complete
last_verified: 2026-08-30
---

# Normalization and Functional Dependencies

## One-Page Review

### Governing question

How can functional dependencies reveal redundancy, guide lossless decomposition, and produce schemas whose constraints remain enforceable without reconstructing the original relation?

### Essential definitions

A **functional dependency** `X -> Y` holds on relation schema `R` when every pair of legal tuples agreeing on attributes `X` also agrees on `Y`. `X+` is the **closure** of `X` under dependency set `F`. A **candidate key** is a minimal `X` with `X+ = R`. A decomposition is **lossless** when joining its projections always recovers exactly the original legal relation, and **dependency preserving** when the projected dependencies imply the original dependencies without a cross-relation join.

### Central model, mechanism, or theorem

Armstrong's reflexivity, augmentation, and transitivity rules are sound and complete for functional-dependency implication. Closure computes implication and keys. Normal forms then constrain determinants: BCNF requires every nontrivial FD determinant to be a superkey; 3NF permits a non-superkey determinant only when every dependent attribute is prime. Binary decomposition of `R` into `R1` and `R2` is lossless under `F` when their intersection functionally determines `R1` or `R2`.

### Critical invariants

- Dependencies come from domain semantics over all legal states, not accidental sample correlations.
- Attribute sets, not column order or names, define determinants and dependents.
- Every claimed candidate key is both determining and minimal.
- Each decomposition is proved lossless; sample reconstruction alone is insufficient.
- Dependency preservation is checked separately from losslessness and normal form.
- Projected keys and foreign keys reconstruct intended associations without spurious tuples.
- Null, temporal, conditional, and probabilistic relationships are not silently modeled as ordinary FDs.
- Denormalization is an explicit later physical/read-model decision, not a failure to derive the logical design.

### Common failures

Failures include discovering FDs from one dataset, treating `A -> B` as causation or invertibility, forgetting composite determinants, computing closure in one pass, calling any identifier a key without minimality, decomposing until duplicates disappear without a lossless proof, assuming BCNF always preserves dependencies, confusing 1NF with “no arrays,” using 2NF when no composite candidate key exists, and enforcing a cross-table dependency only through application code after an avoidable decomposition.

### Compact example

For `R(A,B,C,D,E)` with `A -> BC`, `C -> D`, and `D -> E`, closure gives `A+ = ABCDE`, so `A` is a candidate key. `C -> D` and `D -> E` violate 3NF and BCNF because their determinants are not superkeys and their right sides are non-prime. Decomposition into `ABC`, `CD`, and `DE` is lossless and preserves the displayed dependencies; it stores the facts at the grain where their determinants identify them.

### Connections

[DBE-003](003-schemas-keys-and-constraints.md) establishes key and integrity semantics. [DBE-005](../ROADMAP.md) evaluates deliberate denormalization and read models. Later query, transaction, storage, and distributed modules explain the cost and operational consequences of the logical decomposition.

## Governing Question

A single wide table often repeats facts at different grains. In `Enrollment(student_id, student_name, course_id, course_title, instructor_id, instructor_office, grade)`, a grade describes a student-course enrollment, a course title describes a course, and an office describes an instructor. Repeating them in one row makes one logical fact depend on the existence and multiplicity of unrelated facts.

Normalization is the disciplined process of separating those fact types. It is not a ritual of splitting tables or a promise that joins are cheap. Its formal core asks which attributes determine which others, which dependencies cause redundancy, and whether a proposed set of projections preserves information and enforceable rules.

The governing question therefore has three obligations: infer dependencies from authoritative semantics, select relation boundaries that satisfy a named normal form, and prove both lossless reconstruction and acceptable dependency preservation. A design that satisfies only one obligation can still corrupt or complicate the data.

## Why This Matters

Redundancy creates update anomalies. If a course title appears in 10,000 enrollment rows, renaming it requires 10,000 coordinated changes. A partial update produces disagreement about one course. Deleting the last enrollment may erase the only stored course description. Creating a course before its first enrollment may be impossible because unrelated student fields are required. These are update, deletion, and insertion anomalies caused by co-locating facts with different determinants.

Normalization makes constraints local. Storing `Course(course_id, course_title)` lets the key `course_id` enforce one title row per course. Storing `Enrollment(student_id, course_id, grade)` states enrollment at its own grain. Foreign keys reconnect the facts without copying descriptive values into every enrollment.

Formal analysis matters because intuitive splitting can lose information. Projecting a relation and later joining can invent combinations that never existed. A decomposition can also be lossless yet scatter one dependency across relations so no single constraint can enforce it without a join. Normal form, losslessness, and dependency preservation are distinct properties.

Performance does not invalidate the logical analysis. Production systems may materialize aggregates, duplicate labels, maintain search documents, or build event projections. Those are governed replicas or read models with refresh and reconciliation rules. Starting from a normalized source of truth makes the duplication explicit and testable; [DBE-005](../ROADMAP.md) treats that choice directly.

## Prerequisites and Retrieval

Retrieve sets, subsets, implication, proof by counterexample, relations, projection, natural join, superkeys, candidate keys, and integrity constraints. You should be able to distinguish a schema from one observed instance and a universal claim from a finite test.

Recall from [DBE-003](003-schemas-keys-and-constraints.md) that candidate-key minimality is by set inclusion. This chapter uses concatenated letters such as `AB` for the set `{A,B}`. It assumes classical relations and ordinary equality; SQL null behavior needs additional modeling and is not smuggled into an FD.

## Learning Objectives

After completing this module, you should be able to:

1. state and refute functional dependencies precisely;
2. apply Armstrong's axioms and derived union, decomposition, and pseudotransitivity rules;
3. compute attribute closure to a fixed point;
4. enumerate and prove candidate keys;
5. derive a minimal or canonical cover;
6. diagnose insertion, update, and deletion anomalies from mixed fact grains;
7. distinguish 1NF, 2NF, 3NF, and BCNF using formal definitions;
8. test binary and multi-relation decompositions for losslessness;
9. test dependency preservation using projected dependencies and implication;
10. choose and document a justified 3NF/BCNF boundary for an operational schema.

## Core Exposition

Let `R(U)` be a relation schema with attribute set `U`. A functional dependency `X -> Y`, where `X` and `Y` are subsets of `U`, holds when for every legal instance `r(R)` and every `t1,t2 in r`, `t1[X] = t2[X]` implies `t1[Y] = t2[Y]`. The left side is the **determinant**. The statement is about all legal states allowed by the domain, not just current rows.

An FD is not causal. `postal_code -> municipality` may describe an allocation rule, but it does not say changing a postal code causes a municipality to change. It is not necessarily invertible: many postal codes may map to one municipality. It is not an access path: the database may scan or index. It is a semantic equality constraint.

A single instance can refute an FD: two tuples that agree on `X` and disagree on `Y` are a witness. No finite conforming instance proves the FD for future legal states. Evidence comes from authoritative business rules, standards, identifiers, code contracts, and subject-matter review; profiling is a discovery aid whose candidates require confirmation.

Dependencies can have composite sides. In `Enrollment(student, course, term, grade)`, `(student,course,term) -> grade` may hold while none of the three proper subsets determines grade. Dropping `term` because a sample contains one offering per course silently changes the modeled rule.

An FD `X -> Y` is **trivial** when `Y subseteq X`; it is implied by the definition. A dependency set `F` implies `f`, written `F |= f`, when every relation satisfying all dependencies in `F` also satisfies `f`. The closure `F+` is the set of all implied FDs. Enumerating `F+` is usually unnecessary; attribute closure answers targeted implication questions.

Armstrong's axioms are:

- **Reflexivity:** if `Y subseteq X`, then `X -> Y`.
- **Augmentation:** if `X -> Y`, then `XZ -> YZ` for any `Z`.
- **Transitivity:** if `X -> Y` and `Y -> Z`, then `X -> Z`.

They are sound: every inferred dependency holds in every relation satisfying the premises. They are complete for FDs: every semantically implied FD can be derived. Common derived rules are union (`X -> Y` and `X -> Z` imply `X -> YZ`), decomposition (`X -> YZ` implies both components), and pseudotransitivity (`X -> Y` and `WY -> Z` imply `WX -> Z`).

To compute `X+` under `F`, initialize the closure with `X`. Repeatedly add the right side of any FD whose left side is already contained in the closure. Stop only when a full pass adds nothing. Then `F |= X -> Y` exactly when `Y subseteq X+`. Because `U` is finite and the closure only grows, the procedure terminates.

Candidate keys follow directly. `X` is a superkey when `X+ = U`; it is a candidate key when additionally no proper subset has full closure. Attributes appearing nowhere on any FD right side must occur in every key, because the closure procedure has no other way to introduce them. This gives a lower bound, not necessarily a complete key.

A **prime attribute** belongs to at least one candidate key. Prime status therefore cannot be decided from a single preferred primary key. It matters in 3NF's formal exception.

Dependency sets often contain redundancy. A **minimal cover** has singleton right sides, no extraneous attribute on any left side, and no redundant FD, while remaining equivalent to the original set. A practical procedure splits right sides, tests each left-side attribute by closure without it, then tests each FD by closure under the remaining set. Order can yield different but equivalent minimal covers; equivalence, not textual identity, is the invariant.

Normalization names progressively stronger restrictions.

**First normal form (1NF)** in classical relational theory requires relation-valued facts to be represented through the model's atomic domain values rather than repeating groups embedded in one tuple. “Atomic” is relative to the chosen operators and domain. A date can be one value despite having components; a JSON document can be one SQL value, but hiding facts inside it prevents ordinary relational constraints and dependencies over those subfields unless the product exposes them.

**Second normal form (2NF)** requires 1NF and forbids a non-prime attribute from depending on a proper subset of a candidate key. It addresses partial dependencies on composite keys. If every candidate key is a single attribute, 2NF follows automatically, but transitive redundancy may remain.

**Third normal form (3NF)** has a precise FD definition: for every nontrivial `X -> A` in `F+`, either `X` is a superkey or `A` is prime. The prime-attribute exception enables dependency-preserving synthesis in cases where BCNF cannot preserve every dependency.

**Boyce-Codd normal form (BCNF)** requires for every nontrivial `X -> Y` in `F+` that `X` be a superkey. BCNF removes all FD redundancy of the specified kind inside one relation, but a BCNF decomposition can lose dependency preservation.

Checking only the written FDs is unsafe because normal-form definitions concern implied dependencies. Closure and projected dependencies are therefore central. A schema can appear compliant under a short list while a transitive or augmented implication violates the form.

A **decomposition** of `R(U)` is a collection of schemas `R1(U1),...,Rn(Un)` whose attribute union is `U`. Each legal instance projects to those schemas. The decomposition is **lossless** under `F` when the natural join of all projections equals the original relation for every relation satisfying `F`. Projection followed by join always contains the original tuples; the danger is additional, spurious tuples.

For a binary decomposition `R -> R1,R2`, it is lossless under FDs when `F` implies `(R1 intersect R2) -> R1` or `(R1 intersect R2) -> R2`. The shared attributes must determine all attributes on at least one side. This condition explains why splitting `R(X,Y,Z)` satisfying `X -> Y` into `XY` and `XZ` is lossless: intersection `X` determines `XY`.

For larger decompositions and richer dependencies, use a chase/tableau proof rather than checking pairwise joins casually. A finite sample that happens to rejoin exactly is empirical evidence only; losslessness is universal over legal instances.

A decomposition is **dependency preserving** when enforcing the dependencies projected onto individual `Ri` suffices to imply all of `F`. Formally, if `Fi` contains dependencies in `F+` whose attributes lie within `Ri`, preservation requires the union of all `Fi` to imply `F`. Compute closures under the projected union. If an original FD can be checked only by joining tables, ordinary per-table constraints cannot enforce it directly.

The standard BCNF decomposition step selects a violating FD `X -> Y` and replaces `R` with `XY` and `R - (Y - X)`. The step is lossless because the intersection contains `X`, which determines `XY`. Repeating terminates in BCNF, but dependencies may be lost.

A standard 3NF synthesis begins from a minimal cover, creates one relation for each grouped determinant and its dependents, removes contained schemas, and adds a relation containing a candidate key if none already does. It yields a dependency-preserving, lossless 3NF decomposition. The key relation is necessary for the lossless guarantee; grouping and redundant-schema removal must preserve the synthesis proof.

Normal forms do not discover semantics automatically. A wrong FD can produce a formally perfect decomposition of the wrong world. Temporal rules such as “employee has one manager at a given time,” conditional dependencies such as “for type X, code determines category,” approximate correlations, and multivalued independence require added attributes or stronger dependency formalisms.

## Definitions and Notation

Let `U` be a finite attribute set, `F` a set of FDs, and `r` a legal relation over `U`.

- `X -> Y` holds on `r` iff `forall t1,t2 in r: t1[X]=t2[X] implies t1[Y]=t2[Y]`.
- `F |= X -> Y` means every relation satisfying `F` also satisfies `X -> Y`.
- `F+ = {f | F |= f}`.
- `X+_F = {A in U | F |= X -> A}`.
- `X` is a superkey iff `X+_F = U`; it is a candidate key iff no proper subset is a superkey.
- `A` is prime iff it occurs in some candidate key.
- `pi_V(r)` is the projection of `r` onto `V subseteq U`.
- Decomposition `rho={R1,...,Rn}` is lossless under `F` iff for every `r` satisfying `F`, `join_i pi_Ri(r) = r`.
- `F_i` is the projection of `F+` onto `Ri`; `rho` preserves dependencies iff `union_i F_i |= F`.

Normal-form claims always name the dependency theory in scope. A table can be BCNF under the known FDs and still contain redundancy caused by multivalued or join dependencies.

## Mechanisms, Invariants, or Proof Structure

Use the following review sequence:

1. state the grain and authoritative domain rules;
2. express candidate FDs and retain counterexample evidence;
3. compute closures and all candidate keys;
4. reduce dependencies to an equivalent minimal cover;
5. identify 2NF, 3NF, and BCNF violations from implied FDs;
6. synthesize or decompose with a named algorithm;
7. prove losslessness, not merely sample equality;
8. prove or explicitly waive dependency preservation;
9. map projected keys and foreign keys to executable constraints;
10. validate migration, workloads, and reconciliation separately.

The executable model computes closure and candidate keys for the review example. It projects and naturally joins a finite conforming relation to reproduce the proposed 3NF decomposition. It also constructs a lossy `AB`/`BC` split whose shared `B` value creates two spurious tuples.

<!-- bijux-verify: {"id":"finite-normalization-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"closure_A=ABCDE\nclosure_C=CDE\ncandidate_keys=('A',)\nbcnf_violations=('C->D', 'D->E')\nprojection_sizes=(2, 2, 2)\njoin_recovers=True\nlossy_join_size=4\nspurious_tuples=2\n","stderr":""}} -->
```python
from itertools import combinations


def closure(seed, dependencies):
    result = set(seed)
    changed = True
    while changed:
        changed = False
        for left, right in dependencies:
            if left <= result and not right <= result:
                result |= right
                changed = True
    return frozenset(result)


def candidate_keys(attributes, dependencies):
    ordered = sorted(attributes)
    keys = []
    for size in range(1, len(ordered) + 1):
        for values in combinations(ordered, size):
            proposed = frozenset(values)
            if any(key <= proposed for key in keys):
                continue
            if closure(proposed, dependencies) == attributes:
                keys.append(proposed)
    return tuple("".join(sorted(key)) for key in keys)


def project(schema, rows, selected):
    positions = [schema.index(name) for name in selected]
    return {tuple(row[index] for index in positions) for row in rows}


def natural_join(left_schema, left_rows, right_schema, right_rows):
    shared = [name for name in left_schema if name in right_schema]
    left_key = [left_schema.index(name) for name in shared]
    right_key = [right_schema.index(name) for name in shared]
    right_only = [name for name in right_schema if name not in shared]
    right_append = [right_schema.index(name) for name in right_only]
    schema = tuple(left_schema) + tuple(right_only)
    rows = set()
    for left in left_rows:
        for right in right_rows:
            if tuple(left[i] for i in left_key) == tuple(right[i] for i in right_key):
                rows.add(tuple(left) + tuple(right[i] for i in right_append))
    return schema, rows


attributes = frozenset("ABCDE")
dependencies = (
    (frozenset("A"), frozenset("BC")),
    (frozenset("C"), frozenset("D")),
    (frozenset("D"), frozenset("E")),
)
schema = tuple("ABCDE")
rows = {
    ("a1", "b1", "c1", "d1", "e1"),
    ("a2", "b2", "c2", "d2", "e2"),
}
abc = project(schema, rows, tuple("ABC"))
cd = project(schema, rows, tuple("CD"))
de = project(schema, rows, tuple("DE"))
joined_schema, joined = natural_join(tuple("ABC"), abc, tuple("CD"), cd)
joined_schema, joined = natural_join(joined_schema, joined, tuple("DE"), de)

lossy_schema = tuple("ABC")
lossy_rows = {("a1", "b", "c1"), ("a2", "b", "c2")}
ab = project(lossy_schema, lossy_rows, tuple("AB"))
bc = project(lossy_schema, lossy_rows, tuple("BC"))
_, lossy_join = natural_join(tuple("AB"), ab, tuple("BC"), bc)

print(f"closure_A={''.join(sorted(closure(frozenset('A'), dependencies)))}")
print(f"closure_C={''.join(sorted(closure(frozenset('C'), dependencies)))}")
print(f"candidate_keys={candidate_keys(attributes, dependencies)}")
print("bcnf_violations=('C->D', 'D->E')")
print(f"projection_sizes={(len(abc), len(cd), len(de))}")
print(f"join_recovers={joined == rows and joined_schema == schema}")
print(f"lossy_join_size={len(lossy_join)}")
print(f"spurious_tuples={len(lossy_join - lossy_rows)}")
```

The successful join is a test of one finite relation, not the lossless proof; the intersection/key argument supplies that proof. The lossy counterexample does refute universal losslessness for the displayed `AB`/`BC` decomposition in the absence of a dependency making `B` determine one side. The program does not compute projected dependencies, a minimal cover, a chase, multivalued dependencies, SQL nulls, or physical cost.

## Alternatives and Trade-Offs

**3NF versus BCNF:** BCNF gives the stronger determinant condition and removes more FD redundancy. 3NF synthesis guarantees dependency preservation and losslessness, sometimes retaining controlled redundancy involving prime attributes. Prefer BCNF when critical dependencies remain locally enforceable; prefer a justified 3NF design when preserving them matters more than eliminating the residual pattern.

**Decomposition versus rejection of a dependency:** If an alleged FD is not a durable domain rule, do not normalize around it. Model temporal scope, type conditions, or many-valued facts explicitly. A profiler's near-perfect correlation may guide compression or quality monitoring without becoming schema semantics.

**Normalized write model versus materialized read model:** A normalized system of record localizes truth and updates. A read model may duplicate values to avoid joins or preserve historical snapshots. It then needs ownership, refresh ordering, versioning, repair, and staleness guarantees. Logical normalization and physical co-location can coexist through clustering, indexes, caching, or materialized views.

**Generic identifiers versus compound domain keys:** A surrogate can simplify joins but does not remove FDs among business attributes. Keeping alternate keys and normalized reference relations prevents duplicates while children use compact identifiers.

**Database enforcement versus service boundary:** FDs inside one relation can often become unique/key/check constraints. A dependency spanning tables may require a unique parent plus foreign keys. Across independent services, synchronous enforcement may be unavailable; the design must name asynchronous reconciliation and weaker temporal guarantees.

**Higher normal forms:** BCNF addresses FDs. Fourth normal form addresses nontrivial multivalued dependencies whose determinant is not a superkey. Fifth normal form addresses join dependencies. Do not invoke higher forms as prestige labels; use the dependency class that matches the redundancy.

## Failure Modes and Misconceptions

1. Inferring universal dependencies from a small or historically clean sample.
2. Treating high correlation or low entropy as a functional dependency.
3. Assuming `X -> Y` implies `Y -> X`.
4. Reading an FD as causation or an update instruction.
5. Omitting time, tenant, locale, or type scope from a determinant.
6. Ignoring composite determinants because individual attributes look familiar.
7. Stopping closure after one scan and missing transitive additions.
8. Calling a superkey a candidate key without testing proper subsets.
9. Computing prime attributes from only the chosen primary key.
10. Removing an FD from a cover without checking equivalence.
11. Checking normal form only against the listed FDs rather than `F+`.
12. Applying 2NF language to a schema whose candidate keys are all simple.
13. Explaining 3NF only as “no transitive dependency” and missing its prime exception.
14. Claiming BCNF and 3NF are always equivalent.
15. Assuming a BCNF decomposition preserves every dependency.
16. Assuming a dependency-preserving decomposition is automatically lossless.
17. Treating sample join equality as a universal lossless proof.
18. Joining projections without checking for spurious tuples.
19. Forgetting to add a candidate-key relation during 3NF synthesis.
20. Declaring a decomposition complete without projected keys and foreign keys.
21. Confusing logical relation boundaries with physical files or network calls.
22. Treating JSON, arrays, or structs as inherently non-1NF without stating the domain model.
23. Normalizing derived snapshots that intentionally preserve historical values back to mutable current facts.
24. Denormalizing for assumed performance before measuring joins, indexes, and workload.

## Worked Examples

### Example 1

**Situation:** Does current data with unique `email` prove `email -> customer_id`? **Reasoning:** It is consistent with the FD but future reuse, aliases, tenant scope, and normalization may permit counterexamples. Only a durable rule can establish it. **Conclusion:** Profiling proposes an FD; domain authority confirms or rejects it.

### Example 2

**Situation:** With `A -> B` and `B -> C`, compute `A+`. **Reasoning:** Start `{A}`; add `B`; the new `B` enables `C`; a further pass adds nothing. **Conclusion:** `A+={A,B,C}`, and `A -> C` follows by transitivity.

### Example 3

**Situation:** For `R(A,B,C,D)` with `AB -> C` and `C -> D`, is `AB` a candidate key? **Reasoning:** `(AB)+=ABCD`. `A+={A}` and `B+={B}`, so neither proper subset is a superkey. **Conclusion:** `AB` is a candidate key; the partial dependencies would be tested against non-prime attributes under 2NF.

### Example 4

**Situation:** `Employee(emp_id, dept_id, dept_name)` obeys `emp_id -> dept_id` and `dept_id -> dept_name`. **Reasoning:** Repeating the department name per employee creates update and deletion anomalies. Decompose to `Employee(emp_id,dept_id)` and `Department(dept_id,dept_name)`. Shared `dept_id` determines the Department side. **Conclusion:** The decomposition is lossless and stores the name at department grain.

### Example 5

**Situation:** Decompose rows `(a1,b,c1)` and `(a2,b,c2)` into `AB` and `BC`. **Reasoning:** Both projections share `b`; joining pairs every A with every C, creating four rows. Neither FD `B -> A` nor `B -> C` was stated. **Conclusion:** Two spurious tuples refute losslessness.

### Example 6

**Situation:** In `R(A,B,C)` with `AB -> C` and `C -> B`, candidate keys are `AB` and `AC`. **Reasoning:** `C -> B` has determinant `C`, not a superkey, so BCNF fails. Its dependent `B` is prime because `B` belongs to key `AB`, so the 3NF condition passes. **Conclusion:** 3NF can be strictly weaker than BCNF.

### Example 7

**Situation:** A BCNF split makes the dependency `AB -> C` require a join to verify. **Reasoning:** BCNF guarantees lossless decomposition steps, not dependency preservation. If no projected relation contains enough attributes or projected implications to derive `AB -> C`, local constraints are insufficient. **Conclusion:** Evaluate preservation separately and choose BCNF or 3NF deliberately.

### Example 8

**Situation:** Reduce `F={A -> BC, B -> C, A -> B, AB -> C}`. **Reasoning:** Split `A -> BC`; `A -> C` follows through `A -> B` and `B -> C`, so it is redundant. `AB -> C` has extraneous `A` because `B -> C`. An equivalent cover is `{A -> B, B -> C}`. **Conclusion:** Minimal covers remove redundant rules while preserving implication.

### Example 9

**Situation:** `Product(product_id, current_name)` and an invoice line need the sale-time name. **Reasoning:** Replacing the snapshot with a foreign key to the current product would change historical presentation after rename. The invoice fact legitimately includes captured description/version at transaction time. **Conclusion:** Apparent duplication can encode a different temporal fact and is not automatically an anomaly.

### Example 10

**Situation:** A team wants one wide analytics table for latency. **Reasoning:** Keep normalized authoritative relations, define the wide table's grain and derivation, version it, measure freshness, test keys/counts/aggregates, and rebuild from source. **Conclusion:** Governed denormalization is a derived product; it does not erase the normalized source contract.

## Cross-Program Connections

- [Theory of Computation and Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) supplies implication, closure, proof systems, and algorithmic complexity.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) connects closure, key enumeration, covers, and chase procedures to implementation choices.
- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) links normalized aggregates and repositories to ownership and consistency boundaries.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) applies grain, keys, dependencies, and lossless transformations to pipelines and analytical models.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) governs canonical models, semantic contracts, and deliberate duplication across domains.
- Later DBE modules connect decomposition to join execution, query optimization, transactions, indexes, replication, and schema upgrades.

## References

1. E. F. Codd, [“Normalized Data Base Structure: A Brief Tutorial”](https://research.ibm.com/publications/normalized-data-base-structure-a-brief-tutorial), SIGFIDET, 1971. Author-affiliated primary account of normalization and relational simplification.
2. I. J. Heath, [“Unacceptable File Operations in a Relational Data Base”](https://research.ibm.com/publications/unacceptable-file-operations-in-a-relational-data-base), SIGFIDET, 1971. Primary analysis connecting dependencies, projections, and update side effects.
3. W. W. Armstrong, [“Dependency Structures of Data Base Relationships”](https://dblp.org/rec/conf/ifip/Armstrong74), IFIP Congress, 1974. Bibliographic record for the foundational sound and complete dependency axiom system.
4. P. A. Bernstein, [“Synthesizing Third Normal Form Relations from Functional Dependencies”](https://apollo.inf.upol.cz/~urbanec/teaching/2021/data2/files/bernstein.pdf), *ACM TODS* 1(4), 1976. Primary 3NF synthesis procedure and proof context.
5. Ronald Fagin, [“Multivalued Dependencies and a New Normal Form for Relational Databases”](https://research.ibm.com/publications/multivalued-dependencies-and-a-new-normal-form-for-relational-databases), *ACM TODS*, 1977. Author-affiliated primary extension from FDs/BCNF to fourth normal form.
6. Christos Faloutsos, [“Schema Refinement and Normalization — Functional Dependencies”](https://www.cs.cmu.edu/~christos/courses/dbms.S12/slides/17NormI.pdf), Carnegie Mellon University 15-415. Institutional graduate database teaching material on anomalies, FDs, keys, and normal forms.
7. PostgreSQL Global Development Group, [PostgreSQL 18: Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html), official documentation, checked 2026-08-30. Current implementation context for keys, uniqueness, foreign keys, checks, and their operational semantics.

## Exercises

### Exercise 1

For `R(A,B,C,D,E)` with `F={AB -> C, C -> D, D -> E}`, compute `(AB)+` and determine whether `AB` is a candidate key, showing minimality.

### Exercise 2

Use Armstrong-style reasoning to show that `A -> BC` and `C -> D` imply `A -> D`. Name each intermediate rule.

### Exercise 3

For `Assignment(employee, project, project_manager, hours)` with `(employee,project) -> hours` and `project -> project_manager`, identify the anomaly, normal-form violation, and a lossless decomposition.

### Exercise 4

For `R(A,B,C)` with `F={AB -> C, C -> B}`, compare 3NF and BCNF, and explain the dependency-preservation trade-off of decomposing on `C -> B`.

### Exercise 5

A profiler reports `device_id -> firmware_version` with 99.999% confidence. Devices may upgrade over time and records contain event timestamps. Redesign the dependency claim and schema so it represents the domain truth.

## Answers to the Exercises

### Answer 1

Start with `{A,B}`. `AB -> C` adds `C`; `C -> D` adds `D`; `D -> E` adds `E`. Thus `(AB)+={A,B,C,D,E}`, so `AB` is a superkey. `A+={A}` and `B+={B}` because no dependency fires from either alone. Therefore neither proper subset is a superkey, and `AB` is a candidate key.

### Answer 2

Decompose `A -> BC` to obtain `A -> C`. With `C -> D`, transitivity yields `A -> D`. Equivalently, closure begins with `A`, adds `B,C`, then adds `D`. The conclusion is logical implication under the two premises, not evidence that `A` causes `D`.

### Answer 3

The manager repeats for every assignment on one project. Updating a manager can create inconsistent copies, and deleting the final assignment can erase the manager fact. Candidate key `(employee,project)` determines all attributes, while `project -> project_manager` has a non-superkey determinant and non-prime dependent, violating 2NF as a partial dependency and therefore also 3NF/BCNF. Decompose to `Assignment(employee,project,hours)` and `Project(project,project_manager)`. Intersection `project` determines the Project relation, so the binary decomposition is lossless; both displayed dependencies remain local.

### Answer 4

Candidate keys are `AB` and `AC`, so all three attributes are prime. `C -> B` violates BCNF because `C+={B,C}` and `C` is not a superkey. It satisfies 3NF because dependent `B` is prime. A BCNF split into `CB` and `AC` is lossless since shared `C` determines `CB`, but `AB -> C` is not implied by dependencies local to those projections. Remaining in 3NF preserves the dependency in one relation; choosing the BCNF split requires a cross-relation enforcement strategy or an explicit waiver.

### Answer 5

The reported relationship is not the timeless FD `device_id -> firmware_version`; one device can legally have several versions across events. If at most one version is active at an instant, model `DeviceFirmware(device_id, effective_from, effective_to, firmware_version)` with temporal non-overlap and a key such as `(device_id,effective_from)`, or store immutable events keyed by `(device_id,event_time,event_id)`. A snapshot relation may enforce one current row per device separately. Confirm ordering, late events, clock semantics, and rollback. The 99.999% profile is evidence about observed data quality, not the domain dependency.
