---
module_id: DBE-061
program: Database Engineering
level: 2
module_number: 61
title: Relational Rewrite Rules
status: complete
last_verified: 2026-08-30
---

# Relational Rewrite Rules

## One-Page Review

### Governing question

How can a database optimizer transform a bound relational expression into alternatives that are observably equivalent, expose cheaper execution opportunities, and still terminate under SQL's bags, nulls, errors, effects, ordering, and policy boundaries?

### Essential definitions

A **relational expression** is a typed logical operator tree or graph. A **rewrite rule** has a left pattern, semantic guard, and replacement. A matched occurrence is a **redex**. A rule is **sound** under contract C when every guarded application preserves C's observable result for every legal database state. A **normalization rule** selects a canonical form; an **exploration rule** introduces an equivalent alternative without claiming it is cheaper. A **rewrite strategy** controls match order, repetition, budgets, and phases. A **normal form** admits no selected rule. **Termination** excludes infinite rewrite sequences; **confluence** means divergent sequences can rejoin. A **memo** stores equivalence classes and physical-property variants so alternatives can be shared rather than destructively rewritten.

### Central model, mechanism, or theorem

Write `E ≡C E'` when observations of E and E' agree for every legal input under semantic contract C. A rule `L -> R if G` is sound when `G(theta,D)` implies `Ltheta ≡C Rtheta` for every well-typed substitution theta and legal state D. Sound local replacement is compositional only for contexts that preserve the same observations. An optimizer therefore needs a semantic contract, proven or reviewed side conditions, binding-safe substitution, a terminating/saturating strategy, and an independent chooser. Equivalence does not imply improvement, and reaching a normal form does not imply global optimality.

### Critical invariants

- Input and output schemas, types, collations, names/ordinals, nullability, bags, and requested order remain compatible with the contract.
- SQL TRUE, FALSE, and UNKNOWN are not replaced by two-valued Boolean laws without proof.
- Duplicate-sensitive operators, outer joins, aggregation, windows, limits, recursion, and set operators act as rewrite barriers unless a rule has exact side conditions.
- Volatile, stateful, nondeterministic, throwing, security-sensitive, and resource-observable expressions are neither duplicated, discarded, nor moved illegally.
- Column references use stable binding identities; substitution cannot capture names or silently change correlated scope.
- Constraint-based rules consume only constraints valid for the query snapshot and enforcement mode.
- Rule application terminates by a well-founded measure, bounded strategy, or memo saturation with deduplication.
- Logical equivalence and physical cost selection remain separate claims; every chosen plan is revalidated against required properties.

### Common failures

Typical failures are importing set laws into bag SQL; pushing a right-side predicate below a left join; eliminating a join from an unenforced key; folding a mislabeled volatile function; changing error or call multiplicity; dropping an ordering needed by limit/window; confusing expression equality with textual equality; losing field bindings during projection; oscillating between inverse rules; expanding alternatives exponentially; trusting differential tests as proof; or allowing rewrites to cross row-security, masking, tenant, remote-capability, or snapshot boundaries.

### Compact example

For bag R, `sigma_p(sigma_q(R))` equals `sigma_(p AND q)(R)` when p and q are safe predicates under the stated evaluation contract. But `sigma_(S.flag='open')(R LEFT JOIN S)` is not generally equal to `R LEFT JOIN sigma_(flag='open')(S)`: an unmatched R row is removed by the first query's WHERE predicate but null-extended and retained by the second. The executable finite model checks three valid bag laws and exposes duplicate-elimination and left-join pushdown counterexamples.

### Connections

Retrieve [Relational Model and Relational Algebra](002-relational-model-and-relational-algebra.md), [Joins and Join Semantics](012-joins-and-join-semantics.md), [Logical and Physical Plans](051-logical-and-physical-plans.md), and [Profiling a Query Operator Pipeline](060-profiling-a-query-operator-pipeline.md). Continue through [the roadmap](../ROADMAP.md) to predicate/projection pushdown, statistics, cardinality, costs, join ordering, access paths, plan caching, and adaptation.

## Governing Question

SQL states what result is wanted while deliberately leaving much of the access procedure open. The optimizer exploits that freedom by replacing one logical expression with another that denotes the same observable computation but exposes a better physical plan. What exactly must remain the same, which assumptions justify each replacement, and how can hundreds of interacting rules run without silently changing answers or exhausting planning resources?

The phrase “algebraic identity” is necessary but insufficient. Classical relational algebra uses sets, total predicates, no null marker, no volatile calls, no errors, and no intrinsic order. Production SQL commonly has bags, three-valued logic, type coercions, collations, outer joins, aggregates, windows, limits, lateral correlation, recursive terms, functions with effects, authorization filters, and remote sources with partial semantics. A rewrite rule is engineering code around a theorem whose assumptions must be represented and checked.

The goal is not one canonical list of tricks. It is a durable method for specifying, proving, implementing, testing, scheduling, observing, and retiring relational rewrites. The method must distinguish semantic soundness from profitability: an equivalent expression can be catastrophically slower, while a fast expression that changes one duplicate, null, exception, side effect, or protected row is incorrect.

## Why This Matters

Rewrites create the search space in which cost-based optimization operates. A predicate above a join may hide an indexable restriction. A projection that carries unused wide values may force unnecessary reads, serialization, exchange, and spill. A correlated subquery may imply repeated work until decorrelation exposes a join. A contradictory predicate can replace an entire subtree with an empty relation. Join associativity can produce many logically equivalent trees with radically different intermediate cardinalities.

The historical Starburst query-rewrite work separated a production-rule transformation facility from later plan optimization and showed that rule-based rewrites could unlock orders-of-magnitude execution improvements for some queries. Cascades generalized optimizer search around rules, equivalence groups, physical properties, costs, and guidance. Current Apache Calcite documentation still describes planner rules as transformations to equivalent relational expressions and distinguishes dynamic-programming Volcano search from a more fixed-order heuristic planner. These are architectural ideas, not product recipes.

The same power creates correctness risk. An optimizer defect is unusual software: it can return plausible but wrong rows only for a rare combination of join kind, nullability, constraint metadata, function volatility, and rule order. A hand-tested example rarely covers that state space. Current PostgreSQL 18 documentation treats function volatility as a promise to the optimizer and warns that Boolean subexpression evaluation order is not defined. Its 18.2 release notes include an incorrect pushdown involving volatile or set-returning grouping expressions—concrete evidence that side conditions are not academic decoration.

Rewrite engineering is also resource governance. Two individually terminating rules can oscillate when composed. A sound commutativity rule can enumerate factorially many join trees. A canonicalizer can destroy a shape needed by another rule. Remote pushdown can transfer sensitive predicates or evaluate them under a different collation, time zone, null convention, or authorization context. Planning must therefore have budgets, deterministic diagnostics, capability contracts, and safe fallback.

## Prerequisites and Retrieval

You should know relational algebra, SQL bag and null semantics, inner and outer joins, grouping, subqueries, logical versus physical plans, expression trees, types and collations, keys and constraints, and basic proof by extensional equality. You should be able to trace a small Python program and reason about termination measures.

Retrieve these distinctions before proceeding: set versus bag; TRUE/FALSE/UNKNOWN; schema identity versus display name; inner versus outer join; WHERE versus ON; deterministic versus volatile; total versus partial/throwing expression; logical property versus physical trait; rule soundness versus profitability; destructive normalization versus equivalence exploration; termination versus confluence; proof versus bounded model check; query rewrite versus PostgreSQL's separately named rule system; and required versus delivered properties.

DBE-002 established algebraic equivalence. DBE-012 established join semantics. DBE-051 distinguished logical expressions from executable plans, and DBE-060 established the evidence boundary. This chapter makes transformations precise; DBE-062 through DBE-070 use them in progressively richer optimization decisions.

## Learning Objectives

After this module, you can:

1. specify observational equivalence for a relational rewrite rather than relying on syntax;
2. write a rule as pattern, guard, replacement, phase, and proof obligation;
3. derive selection, projection, join, constant, contradiction, and constraint-based rewrites with side conditions;
4. explain why bags, nulls, outer joins, aggregation, windows, limits, volatility, and errors invalidate naive laws;
5. preserve binding identity, schema, types, nullability, collation, lineage, and required physical properties;
6. compare ordered normalization with memoized equivalence exploration;
7. establish termination using measures, canonical orientation, budgets, or saturation;
8. test rules with exhaustive finite models, metamorphic properties, differential execution, fuzzing, and regression plans;
9. diagnose rule interactions, search explosion, and unsafe metadata assumptions; and
10. design a production rule lifecycle with observability, rollout, fallback, and security boundaries.

## Core Exposition

**Define the observation before equivalence.** Let D range over legal database states, theta over well-typed pattern substitutions, and `Obs_C(E,D)` be the result of evaluating expression E under contract C. Contract C may observe output schema, bag multiplicities, nulls, row order when requested, errors, function-call multiplicity, effects, authorization decisions, and snapshot behavior. Then `E ≡C E'` means `Obs_C(E,D) = Obs_C(E',D)` for every legal D. A narrower optimizer may intentionally define fewer observations, but it must not silently omit something the language or platform promises.

A rewrite rule consists of:

- a typed **left pattern** L with metavariables for operators, expressions, relations, and columns;
- a decidable **match** that binds those metavariables at a redex;
- a **guard** G checking attributes, null rejection, determinism, constraints, correlations, capabilities, and phase state;
- a **replacement** R that constructs a well-bound expression;
- a **semantic contract** and proof/review record;
- a strategy annotation: normalization, exploration, implementation, cleanup, or target pushdown;
- a benefit or promise estimate used only to schedule search, not to establish correctness; and
- stable diagnostics: rule identity, input/output digest, guard result, elapsed work, and budget effect.

The soundness obligation is `G(theta,D) => Ltheta ≡C Rtheta`. Testing several theta and D values can falsify this claim but cannot prove the universal. Proof usually proceeds operator by operator from denotational semantics, with explicit cases for UNKNOWN, null extension, duplicates, and empty input.

**Start with typed, bound expressions.** Rules should normally run after name resolution and type checking. Textual `a` is not an identity: nested queries can shadow it, joins can duplicate names, and projections renumber fields. Bind references to stable relation/column or expression IDs and rebuild mappings when operator schemas change. Preserve casts, collation, time zone, overflow behavior, and nullability. Capture-avoiding substitution is as important in a query optimizer as in a compiler.

**Selection laws need an effect contract.** For total deterministic predicates under ordinary WHERE filtering, a cascade can combine: `sigma_p(sigma_q(R)) ≡ sigma_(p AND q)(R)`. Selections can commute under the same assumptions. A predicate mentioning only R attributes can move below an inner join of R and S. These laws reduce rows earlier and expose access paths, but they do not grant a fixed evaluation order. If p or q can throw, mutate state, read volatile state, or has externally visible call counts, regrouping or duplicating it can change observations.

SQL's UNKNOWN is rejected by WHERE like FALSE, but Boolean identities still require three-valued review. `x = 5 OR x <> 5` is UNKNOWN, not TRUE, when x is null. Replacing it by TRUE admits null rows. Null-rejecting analysis is therefore a semantic property, not a string-pattern heuristic.

**Projection laws track dependencies and multiplicity.** A projection of A after a projection retaining A and B can often be fused to one projection of A. Pushing projection toward scans can reduce width, yet every attribute needed by later predicates, joins, grouping, ordering, windows, authorization, row identity, and computed expressions must remain. Under `DISTINCT`, set operators, or duplicate-sensitive aggregation, moving or deleting a duplicate-elimination boundary can change multiplicities. Expression projections may also change error/call frequency when duplicated or removed.

**Inner joins provide broad but guarded equivalences.** Inner equijoins can commonly commute and associate when predicates are remapped to the correct bindings and the output schema/order contract is restored by projection. Those rules generate alternative join graphs; DBE-066 will address enumeration and cost. Outer, semi, anti, mark, lateral, temporal, and as-of joins have different laws. A filter on the null-supplying side of a left join can convert it to an inner join only when the predicate is proven null-rejecting and movement preserves ON-versus-WHERE meaning. Full outer joins are more restrictive still.

**Aggregation is not ordinary projection.** Pushing aggregation through a join requires knowledge of group keys, join multiplicity, null extension, and the aggregate's decomposability. `SUM` and `COUNT` can use partial states with careful combination; `AVG` requires at least sum and count; holistic aggregates may not admit bounded partial state. Even distributive aggregates can be multiplied by a many-to-many join. A key/foreign-key proof may permit preaggregation, but only if constraints are valid and unmatched/null behavior is preserved.

Windows, ORDER BY, LIMIT/OFFSET, top-k, and recursion impose sequence or fixpoint semantics. Pushing a filter below `row_number`, changing the input of a limit, or reordering a recursive term can change which rows exist or their assigned positions. Treat these operators as barriers until a purpose-built theorem applies.

**Constant folding is evaluation.** Folding `2 + 2` is safe under the exact numeric type and overflow semantics. Folding a function requires its volatility, snapshot, locale, time zone, collation, configuration, error behavior, and plan-cache lifetime to permit it. PostgreSQL 18 categorizes functions as VOLATILE, STABLE, or IMMUTABLE and warns that an incorrect IMMUTABLE label can freeze stale values in reused plans. A rule must trust only metadata whose contract is strong enough, and extension authors become part of the trusted computing base.

**Constraints strengthen the theory.** Valid NOT NULL, CHECK, unique, primary-key, foreign-key, functional-dependency, partition, and domain constraints can prove contradiction, redundant predicates, cardinality upper bounds, join elimination, or outer-to-inner simplification. The guard must know whether a constraint is enforced, validated, deferrable, transaction-visible, partial, conditional, or only informational. An optimizer cannot turn “usually true in production data” into a universal rewrite premise.

Security predicates, row-level access control, masking, audit calls, and tenant boundaries are semantic operators even when hidden from SQL text. A rewrite may not remove, duplicate, reorder across, or push these into a remote system unless the policy model explicitly permits it. Leakproofness and timing/resource observability may matter. Treat data-source capability claims—operators, collations, nulls, numeric ranges, time zones, authorization, snapshot consistency—as versioned contracts.

**Choose a strategy.** An ordered heuristic engine applies phases such as simplify expressions, normalize filters, prune columns, decorrelate, and clean up. It is predictable and budgetable, but rule order can miss alternatives and produce different normal forms when the system is nonconfluent. A fixed-point phase repeats until no change; each rule or the phase as a whole needs a decreasing measure, canonical orientation, deduplication, and fuel.

A memoizing optimizer registers logically equivalent expressions in groups rather than replacing one tree forever. Transformation rules expand equivalence; implementation rules introduce physical operators and traits; dynamic programming compares costs for required properties. Sharing avoids rediscovering identical subexpressions, but the alternative space can still explode. Cascades describes guidance mechanisms such as rule promises, pruning, and task ordering. Apache Calcite's current documentation similarly separates correctness of a planner rule from the planner's cost-guided sequence and exposes both Volcano and heuristic planning styles.

Termination and confluence answer different questions. A terminating system can have several irreducible results. A confluent system has a joinable outcome but may not terminate. Query optimizers often do not need a unique syntactic normal form: a memo can retain alternatives and choose by cost. Destructive canonicalizers do benefit from idempotence and canonical orientation—for example, sort conjunction terms by stable digest rather than alternately commute them.

Use a well-founded measure where possible: fewer nested filters, fewer identity projects, smaller expression depth, or lexicographic `(phase violations, nodes)`. An expansion rule cannot decrease node count; constrain it by memo novelty, property need, promise, time/memory budget, and per-rule match limits. Record whether search completed, pruned, timed out, or fell back. A budgeted answer is not the proven global optimum; it is the best legal alternative found under the stated search.

**Build layered validation.** First, manually or mechanically prove the rule over the formal operator semantics. Second, exhaustively enumerate small finite inputs including empty bags, duplicates, nulls, key violations when guards are false, and boundary values. Third, use metamorphic tests: execute source and rewritten queries on generated schemas/data and compare schema, bag/order, errors, and relevant calls. Fourth, differential-test against an independent engine or unoptimized reference where semantics align. Fifth, fuzz matches and rule sequences, minimize counterexamples, and retain seeds. Sixth, maintain regressions for every past optimizer defect.

The executable below is deliberately a finite model, not a SQL implementation or proof. It checks three valid laws for one bag/type fragment and demonstrates two counterexamples. Rows are tuples, Python `None` models only the null extension needed by the example, and predicates are total/pure.

<!-- bijux-verify: {"id":"finite-rewrite-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"bag_rows=4\ncombined_selection_equal=True\nprojection_fusion_equal=True\njoin_commutativity_equal=True\ndistinct_elimination_equal=False\nleft_join_filter_pushdown_equal=False\nvalid_laws_checked=3\ncounterexamples_found=2\nevidence=finite_bag_semantics\n","stderr":""}} -->
```python
from collections import Counter


def select(rows, predicate):
    return [row for row in rows if predicate(row)]


def project(rows, positions):
    return [tuple(row[position] for position in positions) for row in rows]


def bag(rows):
    return Counter(rows)


def inner_join(left, right):
    return [(key, left_value, right_value)
            for key, left_value in left
            for right_key, right_value in right
            if key == right_key]


def left_join(left, right):
    output = []
    for key, left_value in left:
        matches = [(key, left_value, right_value)
                   for right_key, right_value in right if key == right_key]
        output.extend(matches or [(key, left_value, None)])
    return output


rows = [(1, "x", 7), (1, "x", 7), (2, "y", 4), (3, "z", 9)]
p = lambda row: row[0] <= 2
q = lambda row: row[2] >= 7
combined_selection = bag(select(select(rows, p), q)) == bag(select(rows, lambda r: p(r) and q(r)))
projection_fusion = bag(project(project(rows, (0, 1)), (0,))) == bag(project(rows, (0,)))

left = [(1, "L1"), (2, "L2")]
right = [(1, "R1"), (1, "R2")]
forward = inner_join(left, right)
reverse = [(key, left_value, right_value)
           for key, right_value, left_value in inner_join(right, left)]
join_commutativity = bag(forward) == bag(reverse)

bag_projection = project(rows, (0,))
distinct_projection = list(dict.fromkeys(bag_projection))
distinct_elimination = bag(bag_projection) == bag(distinct_projection)

statuses = [(1, "open"), (1, "closed")]
after_join = select(left_join(left, statuses), lambda row: row[2] == "open")
pushed = left_join(left, select(statuses, lambda row: row[1] == "open"))
left_join_pushdown = bag(after_join) == bag(pushed)

print(f"bag_rows={len(rows)}")
print(f"combined_selection_equal={combined_selection}")
print(f"projection_fusion_equal={projection_fusion}")
print(f"join_commutativity_equal={join_commutativity}")
print(f"distinct_elimination_equal={distinct_elimination}")
print(f"left_join_filter_pushdown_equal={left_join_pushdown}")
print(f"valid_laws_checked={sum((combined_selection, projection_fusion, join_commutativity))}")
print(f"counterexamples_found={sum((not distinct_elimination, not left_join_pushdown))}")
print("evidence=finite_bag_semantics")
```

An implementation should emit more than final plans. For each attempted match, make it possible—under bounded diagnostic controls—to recover rule ID/version, expression/group ID, guard facts, produced alternative, property change, suppression reason, planning time/memory, and whether the alternative survived cost pruning. Avoid logging raw literals or protected query text by default. Stable normalized digests and privacy-safe parameter classes support comparison.

Deploy rule changes like compiler changes. Establish semantic corpora and randomized differential suites; benchmark planning time, memo groups/expressions, rule matches, and execution workload; canary by query fingerprint and engine version; compare result digests where safe; bound resource use; and preserve a kill switch or rule exclusion path. A rule that is sound but causes search explosion is still a production defect. A rule that improves one benchmark but regresses parameter classes or concurrency is not generally profitable.

## Definitions and Notation

- **D**: a legal database state, including data, schema, constraints, snapshot, and policy environment.
- **C**: semantic observation contract for a rewrite scope.
- **Obs_C(E,D)**: observable outcome of expression E on D under C.
- **E ≡C E'**: observational equivalence for every legal D under C.
- **theta**: a well-typed substitution from rule metavariables to bound expressions.
- **L, R, G**: left pattern, replacement, and semantic guard of a rule.
- **Redex**: matched subexpression eligible for a rule.
- **Normalization rule**: oriented rewrite intended to reduce expressions to a canonical family.
- **Exploration rule**: rule that adds a logically equivalent alternative to search.
- **Implementation rule**: rule mapping a logical expression to a physical expression with traits.
- **Normal form**: expression with no applicable rules from the selected system/phase.
- **Termination**: absence of an infinite rule-application sequence.
- **Confluence**: ability of divergent rewrite sequences to reach a common successor.
- **Memo group**: equivalence class of expressions with the same logical meaning.
- **Trait/property**: required or delivered ordering, distribution, convention, rewindability, or similar physical condition.
- **Null-rejecting predicate**: predicate that cannot be TRUE when specified referenced inputs are null-extended.
- **Rule fuel**: explicit bound on matches, alternatives, time, memory, or work.

Rule soundness is `for all theta,D: G(theta,D) => Obs_C(Ltheta,D) = Obs_C(Rtheta,D)`. This is different from profitability `Cost(Rtheta) < Cost(Ltheta)`, which depends on estimates and required properties and need not hold universally.

## Mechanisms, Invariants, or Proof Structure

**Local replacement proof.** Define each operator denotationally over typed bags plus the contract's error/effect/order observations. Prove L and R produce the same schema and, for every output tuple, the same multiplicity and values under G. Then prove the enclosing contexts in which the rule fires are congruent for those observations. A hidden security or sequence context can invalidate ordinary congruence.

**Selection-cascade proof.** For each occurrence t in bag R, nested selection retains t iff q(t) is TRUE and p(t) is TRUE. Combined selection retains t iff `p(t) AND q(t)` is TRUE. Under total pure SQL three-valued predicates, these retention conditions agree and neither form changes multiplicity. The proof does not establish identical evaluation order or call count for effectful/throwing predicates.

**Projection-fusion proof.** Let inner projection map tuple t to attributes B and outer projection map B to A, with every A dependency preserved by B. Function composition maps t directly to A. Under bag projection without intermediate duplicate elimination, each input occurrence contributes one output occurrence in both forms. DISTINCT, grouping, errorful expressions, or missing dependencies require a different theorem.

**Join-alternative proof.** For inner joins, characterize an output as a compatible pair or tuple family satisfying the conjunction of join predicates. Commutation or association changes enumeration, not the satisfying combinations, provided bindings/predicates and output schema are remapped. Outer joins additionally synthesize null-extended rows based on absence of matches, so ordinary associativity and predicate movement fail.

**Constraint proof.** A constraint-based rewrite has two premises: the constraint logically entails the guard, and the engine may rely on that constraint for this snapshot/query. Validate both. Metadata marked informational, not validated, deferred, partial, or remote may support estimation but not semantic elimination.

**Termination argument.** For canonical phases, identify a well-founded measure and show every application strictly decreases it. For exploratory phases, deduplicate expressions by semantic/structural key within memo groups and bound novelty, required properties, time, and memory. Test interaction cycles, not just individual rules. Inverse rules belong in memo exploration or separately gated phases, not an unbounded destructive loop.

**Property invariant.** Every alternative carries logical schema/properties and physical delivered traits. A parent requests traits; converters or implementations satisfy them at a cost. Before plan selection, check the root delivers requested order, distribution, convention, rewindability, and other engine-specific properties. Logical equality alone cannot justify dropping a required sort or data-movement boundary.

**Validation argument.** Proof establishes universality within the model. Exhaustive finite checking catches small counterexamples. Fuzzing explores representations and interactions. Differential/metamorphic execution checks the implementation and target semantics. Regression fixtures prevent recurrence. None substitutes for the others, and performance evidence never establishes semantic equivalence.

## Alternatives and Trade-Offs

**Ordered heuristic rewriting** is deterministic, easy to trace, and naturally budgeted. It is sensitive to phase/rule order and can miss a profitable alternative hidden behind a temporary expansion.

**Fixed-point normalization** finds more matches after enabling rewrites. It requires idempotent/canonically oriented rules, cycle detection, and fuel; otherwise benign inverse rules oscillate.

**Memoized cost-based exploration** shares equivalent expressions and selects by properties/cost. It handles interacting transformations systematically but consumes planning CPU/memory and depends on cardinality/cost quality.

**Equality saturation** retains many equal terms in an e-graph before extraction. It reduces phase-order brittleness but needs relational schema/binding/property/effect analyses, careful side conditions, and strict saturation limits. General compiler machinery is not automatically SQL-correct.

**User-authored rules and hints** make domain knowledge available quickly. They enlarge the trusted surface and can become stale as data, engine versions, or remote capabilities change. Prefer declarative constraints and audited extension APIs with versioned semantics.

**Remote pushdown** reduces movement and uses source indexes/compute. It can change semantics or expose sensitive expressions when source collation, nulls, functions, time zones, numeric behavior, authorization, or snapshot guarantees differ. Capability negotiation and local fallback are mandatory.

**Plan forcing or disabling rules** is valuable for diagnosis and emergency containment. It is not a durable substitute for a sound rule, correct metadata, or robust cost model; forced shapes age across releases and workload changes.

## Failure Modes and Misconceptions

1. **“Relational algebra laws apply directly to SQL.”** SQL bags, nulls, errors, effects, and order add obligations.
2. **“A matching syntax pattern is enough.”** Soundness lives in the guard: types, attributes, join kind, null behavior, constraints, and effects.
3. **“Equivalent means faster.”** Equivalence admits alternatives; estimates and physical properties determine expected cost.
4. **“Passing examples prove the rule.”** Tests find counterexamples; only a proof establishes the universal model claim.
5. **“Predicates can always move downward.”** Outer joins, windows, limits, aggregation, correlations, effects, and security create barriers.
6. **“AND evaluates left to right.”** PostgreSQL documents no defined subexpression order; optimizer rewrites may reorganize Boolean expressions.
7. **“Declared constraints are true.”** Validation/enforcement/deferral/snapshot and partial predicates determine whether they are semantic premises.
8. **“Column names preserve identity.”** Shadowing, duplicate names, ordinal changes, and correlation require stable binding IDs and remapping.
9. **“Each rule terminates, so the system terminates.”** Rule composition can oscillate or grow indefinitely.
10. **“A normal form is optimal.”** It is merely irreducible under one chosen system and strategy.
11. **“The memo prevents explosion.”** It deduplicates alternatives but can still grow beyond useful resource bounds.
12. **“DISTINCT is harmless cleanup.”** Duplicate elimination changes bag semantics and can change aggregates, windows, limits, and joins.
13. **“Remote SQL means identical SQL.”** Dialects and execution environments differ in observable semantics and policy.
14. **“An optimizer kill switch fixes correctness.”** It contains impact; the faulty guard, metadata, representation, or interaction still needs repair and regression evidence.

## Worked Examples

### Example 1

**Combining selections under bag semantics.**

Bag R contains `(1)` twice, `(2)` once, and null once. Let p be `x >= 1` and q be `x <= 1`; UNKNOWN is rejected. Nested selection keeps the two `(1)` occurrences. `p AND q` is TRUE exactly for the same occurrences, so combined selection keeps multiplicity two. Conclusion: cascade combination is sound for these total pure predicates and preserves bags, including duplicate counts.

### Example 2

**A two-valued tautology fails on null.**

Consider `x = 5 OR x <> 5`. For x=5 it is TRUE; for x=7 it is TRUE; for null both comparisons are UNKNOWN and UNKNOWN OR UNKNOWN is UNKNOWN. WHERE rejects that row. Rewriting the predicate to TRUE would retain it. Conclusion: excluded-middle simplification is unsound for nullable SQL comparisons unless a non-null premise or appropriate SQL operator supplies the missing guard.

### Example 3

**Projection pruning needs hidden dependencies.**

A plan reads `(tenant_id, customer_id, amount, created_at)`, filters by `tenant_id`, groups by customer, orders by maximum `created_at`, and returns customer plus sum. Although tenant and timestamp are absent from the final output, tenant is required by policy/filtering and timestamp by aggregate/order computation. Amount and customer are also required. Conclusion: a projection-pruning rule uses transitive expression, policy, grouping, and ordering dependencies, not the final select list alone.

### Example 4

**Filter movement across a left join.**

R has keys 1 and 2; S has `(1,open)` and `(1,closed)`. Filtering `S.flag='open'` in WHERE after `R LEFT JOIN S` returns only key 1/open because the key-2 null-extended row yields UNKNOWN. Filtering S first and then left joining returns key 1/open plus key 2/null. Conclusion: naive right-side pushdown is unsound; a guarded outer-to-inner conversion or different ON placement needs a separate proof.

### Example 5

**Join elimination from a trusted key.**

Query Q inner-joins child C to parent P on non-null `C.parent_id=P.id` and projects only C attributes. If P.id is enforced unique and every C.parent_id has an enforced, snapshot-valid foreign-key match, each C occurrence matches exactly one P occurrence; removing P preserves C's bag. If the foreign key is unvalidated or nullable, unmatched/null child rows invalidate the proof. Conclusion: join elimination is a constraint theorem with enforcement and nullability guards.

### Example 6

**Volatility blocks constant folding.**

Suppose an extension labels `exchange_rate('SEK','EUR')` IMMUTABLE although its table changes daily. The planner folds it while preparing a reusable plan; tomorrow's execution reuses yesterday's value. PostgreSQL's volatility contract explicitly permits folding true immutable calls, so the defect is the false declaration. Conclusion: function metadata is trusted semantic input, and extension validation must test plan-cache lifetime as well as one execution.

### Example 7

**Two terminating rules oscillate together.**

Rule A orders equality constants left: `x=5 -> 5=x`. Rule B orders column references left: `5=x -> x=5`. Each application finishes, but an unrestricted fixed-point phase alternates forever. Choose one canonical ordering key, make the rule idempotent, or deduplicate the expression and stop revisiting it. Conclusion: system termination is a property of rules plus strategy, not of each rule in isolation.

### Example 8

**Aggregate pushdown multiplies values.**

Orders O has one order worth 100; Lines L has three lines for it. Joining and then summing `O.total` returns 300, while summing O before the join yields state 100 that is still repeated if naively joined. Preaggregation is safe only with a combination design that accounts for join multiplicity or when the join is proven one-to-one for the aggregated side. Conclusion: aggregate decomposability alone is insufficient; keys and multiplicity are premises.

### Example 9

**Memo exploration versus destructive swapping.**

For inner joins A, B, C, commutation and association can produce several trees. Repeatedly replacing the current tree loses alternatives and may cycle. A memo registers each equivalent expression under one logical group, associates property variants/costs, and chooses a winner under a planning budget. Conclusion: bidirectional equivalences belong naturally in shared exploration, while destructive normalization needs one orientation.

### Example 10

**Production diagnosis of a rule regression.**

After an engine upgrade, one fingerprint returns fewer rows only when a nullable dimension and row-security policy are active. Disable one rule in a controlled replica: results match the reference. Trace shows a filter moved below a policy-bearing left join because nullability metadata ignored null extension. Contain with the rule kill switch, minimize a schema/data counterexample, repair the guard and property propagation, add exhaustive null/policy regression cases, canary result digests, and then re-enable. Conclusion: a production response joins semantic containment, minimized evidence, root-cause proof, interaction tests, and staged rollout.

## Cross-Program Connections

- [Programming Languages — Functional Programming](../../03-programming-languages-functional-programming/ROADMAP.md): equational reasoning, purity, substitution, effects, and fixed points explain why optimizer laws need semantic guards.
- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md): typed IRs, dataflow facts, rewrite passes, SSA identity, phase ordering, and validation are close analogues.
- [Theory of Computation and Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md): term rewriting, termination, confluence, search complexity, and proof obligations frame rule systems.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md): hash-consing, DAGs, union/find-like equivalence management, priority queues, and persistent structures support memo implementation.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): semantic contracts, lineage, policy, and federated ownership constrain cross-source transformations.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): capability negotiation, versioned behavior, observability, canaries, and rollback apply to optimizer extensions and remote pushdown.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): resource budgets, multitenancy, safe rollout, kill switches, and audit evidence turn rules into an operable subsystem.

## References

1. Hamid Pirahesh, Joseph M. Hellerstein, and Waqar Hasan, [“Extensible/Rule Based Query Rewrite Optimization in Starburst”](https://research.ibm.com/publications/extensiblerule-based-query-rewrite-optimization-in-starburst), *SIGMOD 1992*. Primary query-rewrite architecture, rule classes, and production-rule scheduling.
2. Goetz Graefe, [“The Cascades Framework for Query Optimization”](https://liuyehcf.github.io/resources/paper/The-Cascades-Framework-For-Query-Optimization.pdf), *IEEE Data Engineering Bulletin* 18(3), 1995. Primary memoized rule/property/cost search framework.
3. Apache Calcite Project, [Algebra](https://calcite.apache.org/docs/algebra.html), retrieved 2026-08-30. Current relational-expression and semantics-preserving planner-rule documentation.
4. Apache Calcite Project, [Adapters: Planner Rule, Calling Conventions, Statistics and Cost](https://calcite.apache.org/docs/adapter), retrieved 2026-08-30. Current rule correctness, planner styles, pushdown capability, traits, and metadata documentation.
5. PostgreSQL Global Development Group, [PostgreSQL 18: Function Volatility Categories](https://www.postgresql.org/docs/18/xfunc-volatility.html), retrieved 2026-08-30. Current optimizer promises for VOLATILE, STABLE, and IMMUTABLE functions.
6. PostgreSQL Global Development Group, [PostgreSQL 18: Value Expressions—Expression Evaluation Rules](https://www.postgresql.org/docs/18/sql-expressions.html#SYNTAX-EXPRESS-EVAL), retrieved 2026-08-30. Current Boolean reorganization, evaluation-order, side-effect, and early-folding constraints.
7. PostgreSQL Global Development Group, [PostgreSQL 18: Query Planning](https://www.postgresql.org/docs/18/runtime-config-query.html), retrieved 2026-08-30. Current planner controls, self-join elimination, costs, search, and constraint exclusion.
8. PostgreSQL Global Development Group, [PostgreSQL 18: The Rule System](https://www.postgresql.org/docs/18/rules.html), retrieved 2026-08-30. Current distinction and pipeline role of PostgreSQL's query rewrite rule system.
9. DuckDB Foundation, [Overview of DuckDB Internals](https://duckdb.org/docs/current/internals/overview.html), retrieved 2026-08-30. Current binder, logical-plan, expression-rewrite, filter-pushdown, join-order, and physical-plan pipeline.
10. DuckDB Foundation, [`optimizer.cpp`](https://github.com/duckdb/duckdb/blob/main/src/optimizer/optimizer.cpp), reviewed 2026-08-30 at the current main branch. Primary implementation evidence for optimizer phase ordering and guarded transformations; branch-relative and therefore not a stable release interface.
11. PostgreSQL Global Development Group, [PostgreSQL 18.2 Release Notes](https://www.postgresql.org/docs/18/release-18-2.html), retrieved 2026-08-30. Primary current defect record for an unsafe restriction pushdown involving volatile and set-returning grouping expressions.

## Exercises

### Exercise 1

State the full soundness obligation for combining two filters. Identify schema, bag, null, error, volatility, and evaluation-order premises; distinguish which are language observations and which are optimizer policy choices.

### Exercise 2

For R=`[(1,a),(2,b)]` and S=`[(1,x)]`, calculate both `(R LEFT JOIN S) WHERE S.value='x'` and `R LEFT JOIN (S WHERE S.value='x')`. Then give a sound transformation involving an inner join and state its guard.

### Exercise 3

A fixed-point optimizer has rules `Project(A,Project(B,X))->Project(A,X)` when dependencies allow, identity-project insertion for a physical adapter, and identity-project removal. Explain the cycle/search risks and design phase, measure, and memo/budget controls.

### Exercise 4

Compare an ordered heuristic planner and memoized exploration for a six-way inner join with filters, one remote source, and a required final order. Specify semantic, capability, property, cost, and resource evidence needed to choose an architecture.

### Exercise 5

Design a release gate for a new outer-join simplification rule in a multitenant database platform. Cover proof, finite models, generated testing, metadata faults, security policies, planning budgets, execution performance, observability, canarying, containment, and evidence limits.

## Answers to the Exercises

### Answer 1

For bound bag expression X and predicates p,q, require `for all legal D: Obs_C(Filter(p,Filter(q,X)),D)=Obs_C(Filter(p AND q,X),D)`. Both sides keep the same schema/types/names and each input occurrence with the same multiplicity exactly when q and p are TRUE versus their SQL conjunction is TRUE. Review FALSE/UNKNOWN truth cases and nullable inputs. If C observes errors, side effects, volatile reads, call counts, or order, require p and q to be total and pure/stable enough that regrouping does not change those observations; otherwise forbid the rule or narrow C only if the language truly permits that narrowing. Bag multiplicity and SQL null behavior are language semantics. Canonical conjunct order, whether to preserve call count beyond the language promise, and profitability thresholds are explicit optimizer/platform policies. Stable binding and type/collation equivalence are representation premises.

### Answer 2

The left join first yields `(1,a,x)` and `(2,b,NULL)`. WHERE `S.value='x'` keeps `(1,a,x)` and rejects the null-extended row because the comparison is UNKNOWN. Filtering S first leaves `(1,x)`; left joining still yields `(1,a,x)` and `(2,b,NULL)`. Thus the proposed pushdown is unequal. A sound alternative is `(R LEFT JOIN S) WHERE S.value='x' -> R INNER JOIN (S WHERE S.value='x')` when the predicate references only S, is null-rejecting for the null-extended S columns, and is total/pure with compatible bindings/types/collation and no security/effect barrier. Null rejection proves every surviving row had a real S match, so inner join is sufficient.

### Answer 3

Projection fusion/removal can decrease logical nesting, but adapter insertion recreates the identity project; unrestricted phases oscillate. Run logical projection fusion/pruning to fixed point before physical conversion, using a measure such as `(nested logical projects, unused fields, nodes)` that strictly decreases. Do not insert physical adapter identities until a convention/property is requested; tag them by convention so logical cleanup does not remove required boundaries. In a memo, store logical equivalence separately from physical implementations and deduplicate structural expressions. Bound group expressions, rule matches, time, and memory; record suppression/fallback. Make identity removal idempotent and ensure any insertion has a monotone unmet-property premise. Add an interaction regression that executes the complete phase schedule, not only each rule.

### Answer 4

An ordered heuristic planner offers bounded, traceable filter/projection pushdown and may suit strict latency budgets, but one chosen join order can miss major alternatives. Memoized exploration represents join commutation/association and local/remote implementations by equivalence group and required traits, improving opportunity at greater planning cost. Both need proofs for inner-join/filter rules, stable bindings, bag/null/effect/policy preservation, and a remote capability contract for functions, collation, time zone, numeric/null semantics, authorization, and snapshot. Required final order must be represented as a root property; remote/local operators declare delivered order/distribution/convention and converters have costs. Compare cardinality/cost accuracy, transfer and remote latency, alternative count, memo memory, planning tails/timeouts, execution distributions, and fallback quality across parameter classes. Choose only after enforcing planning budgets and semantic differential tests; hybrid heuristic preprocessing plus bounded memo search is a defensible design.

### Answer 5

Write the rule's exact left/right forms and guards for join kind, null-rejecting predicate, bindings, predicate purity/totality, nullability, constraints, lateral correlation, and policy barriers. Prove schema and tuple multiplicities by matched and unmatched outer-join cases. Exhaustively enumerate small bags with empty inputs, duplicates, null keys/values, multiple matches, TRUE/FALSE/UNKNOWN, and guard-false cases. Generate typed schemas/data and compare source/rewrite result schema, bag/order, errors, and allowed calls against an unoptimized reference; fuzz rule sequences and minimize retained seeds. Inject stale/unvalidated/deferred constraint facts, wrong nullability, volatile/throwing/set-returning functions, row security, masks, tenant predicates, remote capability mismatch, and snapshot variation. Benchmark rule matches, memo growth, planning CPU/memory/tails/timeouts and execution across scale/parameters/concurrency. Emit privacy-safe rule/plan digests and guard facts. Canary by tenant/fingerprint with result reconciliation where safe, strict resource limits, automatic rollback/kill switch, and a control cohort. Promote only if semantic suites, policy review, budgets, and workload gates pass. State that internal proof/model/tests establish the modeled contract, not universal correctness for extensions, remote engines, undisclosed policies, or production data; named human security/database review is required before claiming external review.
