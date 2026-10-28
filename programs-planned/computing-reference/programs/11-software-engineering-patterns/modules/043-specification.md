---
module_id: SEPAT-043
program: Software Engineering: Patterns
level: 1
module_number: 43
title: Specification
status: complete
last_verified: 2026-08-28
---

# Specification

## One-Page Review

### Governing question

How can a business rule become a named, composable, testable object that answers whether a candidate satisfies a criterion, while evaluation context, explanations, query translation, authorization, time, unknown values, cost, and side effects remain explicit?

### Essential definitions

- A **Specification** is a first-class predicate over candidates, normally exposing `is_satisfied_by(candidate) -> bool` or a richer decision.
- A **leaf specification** implements one atomic domain rule such as `AccountIsActive`.
- A **composite specification** combines specifications with AND, OR, or NOT.
- **candidate** means the object or immutable fact view being classified.
- A **decision** is an allow/match result plus reason, evidence, or indeterminate status when Boolean output is insufficient.
- **query specification** describes a predicate translatable to a data-store query; it is not automatically equivalent to arbitrary in-memory code.
- **remainder predicate** is the part evaluated after a safe coarse query has selected candidates.
- **subsumption** means one specification logically implies another over a stated domain.
- A **policy decision point** evaluates authorization policy with trusted attributes and current context; a generic Specification object is not by itself an authorization system.

### Central model, mechanism, or theorem

For candidate domain (D), a total Boolean specification is a predicate $S:D\to\{T,F\}$. Composite semantics are

$$
(S_1\land S_2)(x)=S_1(x)\wedge S_2(x),\quad
(S_1\lor S_2)(x)=S_1(x)\vee S_2(x),\quad
(\neg S)(x)=\neg S(x).
$$

These laws support equivalence tests only when leaves are pure, total, evaluated over the same snapshot/context, and share two-valued semantics. SQL NULL, remote failures, time changes, side effects, or authorization indeterminacy invalidate naive Boolean rewrites.

### Critical invariants

- Every leaf has one domain name, candidate type, required context, result meaning, and explicit failure/unknown policy.
- Evaluation is pure and deterministic for a fixed candidate/context, or effects and snapshot semantics are elevated into an explicit workflow.
- Combinators preserve order/short-circuit semantics only when those semantics are declared; correctness cannot depend on hidden side effects.
- Boolean, three-valued, error, and explanatory decisions are not silently collapsed.
- In-memory and translated query evaluation agree only over a documented semantic subset and differential evidence.
- Untrusted clients cannot supply arbitrary executable specifications, fields, operators, or authorization facts.
- Time, locale, money, identity, tenant, and version are explicit bounded inputs rather than ambient globals.
- Logs/explanations redact sensitive operands and stay bounded; a match does not prove authorization or safe action.

### Common failures

Common failures include one `GenericSpecification(lambda x: ...)` vocabulary, setters that mutate shared predicates, I/O inside leaves, reading the clock repeatedly, AND/OR precedence bugs, catching failure as false, negating indeterminate into true, empty AND/OR without defined identity, translating arbitrary code to SQL, SQL NULL/collation/time-zone drift, loading an entire table for filtering, N+1 leaf queries, accepting client field names/operators, serializing executable closures, leaking secrets in explanations, using eligibility as authorization, and treating example matches as proof of policy correctness.

### Compact example

Named leaf specifications select active customers with spend at least 100 units. AND, OR, and NOT compose without changing the customer model; a deterministic run identifies Ada and reports that Bea is inactive.

### Connections

[SEPAT-042](042-null-object.md) models valid absence; [SEPAT-044](../ROADMAP.md) turns a complex method into an object. Specification connects to [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), [Database Engineering](../../18-database-engineering/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

Which business question deserves a durable predicate object, and how can its composition, evidence, translation, performance, failure, and evolution semantics remain as clear as the rule's name?

Specification is useful when rules recur, combine, and must travel between domain services or repositories. It is less useful for a one-off local conditional whose extraction would add indirection without domain meaning.

## Why This Matters

Rules such as “active customer,” “shipment eligible for express handling,” and “invoice needs review” otherwise spread across controllers, repositories, UI code, and jobs. Named specifications create a common vocabulary and enable focused tests and composition.

But executable in-memory predicates, database query expressions, validation diagnostics, and security policies have different trust and semantic boundaries. A production design must preserve those boundaries instead of promising one magical rule object that runs everywhere.

## Prerequisites and Retrieval

You should understand predicates, Boolean algebra, object composition, pure functions, SQL NULL, indexes, authorization, and testing. Retrieve these facts:

1. A predicate classifies; a validation may need multiple diagnostics and a transformation may produce a new value.
2. AND and OR short-circuit in many programming languages, but not all query optimizers preserve an observable evaluation order.
3. SQL comparisons involving NULL commonly yield unknown, not ordinary false.
4. Database collation, decimal representation, and time-zone rules can differ from application behavior.
5. Authorization requires trusted subject, resource, action, environment, policy version, and deny/error semantics.
6. A mutable predicate reused across requests is shared state.

## Learning Objectives

After completing this module, you should be able to:

- identify rules that merit named Specification objects;
- implement leaf and composite specifications with explicit contracts;
- distinguish Boolean matching from decisions with reasons, unknown, and error;
- control purity, snapshots, context, cost, and evaluation order;
- translate a safe specification subset to parameterized queries;
- test algebraic laws and in-memory/query semantic parity;
- secure external rule representations and authorization boundaries;
- evolve, version, observe, and review high-consequence specifications.

## Core Exposition

### Extract domain language, not anonymous plumbing

Start with a sentence domain experts use: `CustomerIsActive`, `OrderCanShip`, or `InvoiceRequiresReview`. A reusable specification owns one question and no state transition. Its name should convey business meaning, not implementation such as `LambdaSpec` or `SqlWhereSpec`.

Keep one-off mechanics local. Extraction is justified by reuse, composition, volatility, testing, repository selection, explanation, or policy ownership—not by every `if` statement.

### Define candidate and context

State the candidate type and whether it is a complete aggregate, immutable facts snapshot, projection, or identifier. Passing a partially loaded entity can turn missing data into false.

Make external facts explicit: `EvaluationContext(now, tenant, currency, locale, policy_version)`. Capture one clock instant and one data/policy version for the decision. Do not read ambient clock/configuration from different leaves.

### Keep leaves pure and total where possible

A Boolean leaf should return true or false for every valid candidate/context and not mutate, log, query, or call a service. Purity enables safe reuse, reordering where permitted, caching with complete keys, and algebraic testing.

If evaluation requires I/O, first gather a bounded facts snapshot in a workflow, then evaluate pure rules. Otherwise model asynchronous failure, timeout, retry, cancellation, and partial evidence explicitly; do not hide them behind `is_satisfied_by`.

### Compose with objects

AND, OR, and NOT are Composite over specifications. Define empty identities: conjunction of no predicates is true and disjunction of no predicates is false if the API allows empty collections. Preserve grouping in the object tree and rendered representation.

Avoid mutable `and(spec)` methods that alter a shared instance. Return immutable composites so a base rule can be safely reused across requests and threads.

### Treat short-circuiting as a contract choice

In memory, AND may skip its right child after false; OR may skip after true. This improves cost and can avoid unnecessary sensitive evaluation. Tests can verify that declared order.

Do not rely on short-circuiting to make unsafe leaves valid. A database optimizer may reorder predicates, and a future evaluator may evaluate concurrently. Every translated expression must be valid independently or guarded using backend-safe constructs.

### Upgrade Boolean when reasons matter

`bool` cannot distinguish no-match, unavailable fact, malformed candidate, stale policy, or evaluator failure. Use `Decision(outcome=match|no_match|indeterminate|error, reasons, evidence_refs, policy_version)` when operations or users need the distinction.

Define combination tables. For authorization, NOT(indeterminate) must not become permit. Bound and redact reason trees; they can reveal thresholds, protected attributes, inventory, or fraud controls.

### Separate validation from selection

A validation specification can answer whether one already-valid aggregate meets a criterion, but validation often needs all violations, paths, localization, and repair advice. A fail-fast Boolean composite loses that information.

Use a validation-result abstraction when diagnostics are the product. Use Specification for a named proposition. Do not make rule evaluation mutate the candidate into validity.

### Separate action from classification

`OrderCanShip` should not reserve stock, charge money, or dispatch a shipment. It classifies one snapshot. A command/workflow rechecks required invariants under transaction/concurrency control and performs the action.

A true result can become stale immediately. Version facts and use optimistic/pessimistic controls where state changes depend on the decision.

### Design query translation as a restricted language

Repository specifications may compile an allowlisted abstract syntax tree—field paths, typed constants, comparison operators, Boolean nodes—into parameterized SQL/criteria expressions. Do not inspect arbitrary closures or execute supplied code.

The translator validates field ownership, types, operators, joins, tenant constraints, cardinality, and cost budgets. Values are parameters, never string interpolation. Query capability is narrower than in-memory expressiveness by design.

### Preserve semantic parity

Application and database evaluation can disagree about NULL/unknown, case/collation, Unicode normalization, decimals, timestamps, time zones, overflow, regexes, and relationship multiplicity. Define the supported semantic subset and canonicalize inputs.

Differential-test the same fixtures against in-memory and actual target-engine evaluation. A unit test of generated SQL text is not semantic evidence.

### Split pushdown and remainder safely

If only part of a rule translates, derive a necessary coarse query predicate (Q) such that every true full match is selected by (Q). Then apply remainder (R) in memory: candidate result is $Q\land R$. An overly narrow (Q) creates false negatives.

Bound the candidate set, pagination, memory, snapshot, ordering, and tenant scope. Reject a plan that would load unbounded rows. Report whether filtering was full, hybrid, or unsupported.

### Plan cost and data access

Annotate or estimate required fields, joins, selectivity, and relative cost. Evaluate cheap selective pure leaves before expensive ones only if order is semantically free. Batch fact gathering to prevent N+1 queries.

Caching requires a key containing specification identity/version, normalized parameters, candidate/fact version, tenant, and relevant context. Bound lifetime and invalidate on policy/data change. Never cache authorization solely by user ID.

### Protect external representations

Treat client-supplied filters as untrusted data. Parse a versioned schema with allowlisted fields/operators/types, depth/node/value-size limits, tenant scope, and cost controls. Reject unknown nodes; never deserialize class names or closures.

Separate public filter vocabulary from internal domain fields. Parameterization addresses injection values but not abusive joins, expensive regexes, sensitive field inference, or authorization bypass.

### Keep authorization distinct

Specifications can implement predicates inside an authorization policy engine, but `isEligible` is not `isAuthorized`. The enforcement point supplies authenticated subject, resource, action, environment, tenant, and current policy/version to a decision point; deny/indeterminate/error fail safely.

Never trust a client-composed Specification to grant access. Enforce row/object authorization independently of user filtering and log bounded decision metadata through approved audit paths.

### Explain without leaking

An explanation tree can mirror composite nodes and leaf codes, recording evaluated/skipped/indeterminate status. Give each leaf a stable reason code and separately localized message. Do not embed raw secrets or personal data.

Provide different views for end users, operators, auditors, and developers. Explanations are evidence of evaluator behavior, not proof that source data or policy is correct.

### Version and evolve rules

Persist stable specification type tags, schema version, typed parameters, and policy/rule-set version—not language object graphs. Unknown nodes fail explicitly. Migrations preserve meaning or record deliberate changed semantics.

For time-sensitive historical decisions, retain the facts/policy version and bounded evidence needed for reproduction according to privacy and retention rules. Re-evaluating with today's rule is not historical reconstruction.

### Test by layer

Test each leaf at equivalence partitions and boundaries; test composite truth tables, grouping, identities, short-circuit contract, immutability, and reason propagation. Property-test commutativity/associativity/De Morgan only for pure total Boolean leaves.

Test translator allowlists, parameter binding, NULL/collation/decimal/time semantics, joins, tenant filters, limits, unsupported nodes, and query plans on the actual engine. Mutation tests should catch flipped operators, missing tenant predicates, wrong grouping, and error-to-false collapse.

## Definitions and Notation

Let candidate space be (D), Boolean specifications $S_i:D\to\mathbb{B}$, and richer decisions $\Delta=\{match,no\_match,indeterminate,error\}$. For pure total Boolean specifications:

$$
S\land\top=S,\quad S\lor\bot=S,\quad S\land\neg S=\bot,
$$

and De Morgan's law gives $\neg(S_1\land S_2)=\neg S_1\lor\neg S_2$. These identities do not automatically hold observationally with effects, errors, three-valued logic, or explanation order.

For safe hybrid query planning, coarse query (Q) must be necessary for full predicate (S):

$$
\forall x\in D:\ S(x)\Rightarrow Q(x).
$$

The remainder evaluates only selected candidates and must restore the full decision.

## Mechanisms, Invariants, or Proof Structure

### Specification design procedure

1. Name one domain proposition and define candidate/facts/context/result types.
2. Decide whether Boolean is sufficient; otherwise define explicit decision algebra.
3. Implement pure immutable leaves with boundary, failure, and unknown semantics.
4. Compose through immutable AND/OR/NOT nodes with grouping and identity rules.
5. Separate classification from I/O fact gathering and state-changing commands.
6. Define a restricted versioned query/filter representation and safe translator subset.
7. Verify semantic parity, tenant/authorization enforcement, cost, and explanation redaction.
8. Test leaves, truth/decision tables, laws under their assumptions, backends, evolution, and faults.

### Executable finite model

The following example demonstrates pure two-valued leaf and composite evaluation over immutable-by-convention customer facts. It does not establish database translation, concurrent freshness, authorization, or arbitrary-rule correctness.

<!-- bijux-verify: {"id":"specification-composition","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"eligible=Ada\nbea_active=False bea_not_active=True\n","stderr":""}} -->
```python
class Customer:
    def __init__(self, name, active, spend):
        self.name = name
        self.active = active
        self.spend = spend


class Specification:
    def is_satisfied_by(self, candidate):
        raise NotImplementedError

    def and_with(self, other):
        return AndSpecification(self, other)

    def negate(self):
        return NotSpecification(self)


class ActiveCustomer(Specification):
    def is_satisfied_by(self, candidate):
        return candidate.active


class SpendAtLeast(Specification):
    def __init__(self, minimum):
        self.minimum = minimum

    def is_satisfied_by(self, candidate):
        return candidate.spend >= self.minimum


class AndSpecification(Specification):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate):
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(candidate)


class NotSpecification(Specification):
    def __init__(self, inner):
        self.inner = inner

    def is_satisfied_by(self, candidate):
        return not self.inner.is_satisfied_by(candidate)


customers = [
    Customer("Ada", True, 140),
    Customer("Bea", False, 220),
    Customer("Cy", True, 80),
]
active = ActiveCustomer()
eligible = active.and_with(SpendAtLeast(100))
names = [customer.name for customer in customers if eligible.is_satisfied_by(customer)]
bea = customers[1]
print("eligible=" + ",".join(names))
print(
    "bea_active=" + str(active.is_satisfied_by(bea))
    + " bea_not_active=" + str(active.negate().is_satisfied_by(bea))
)
```

The result follows from (active(Ada)=T) and $spend(Ada)\ge100$; Bea fails active despite sufficient spend, and Cy fails spend despite being active. Negation is safe here because the leaf is pure, total, and two-valued.

## Alternatives and Trade-Offs

- **Local conditional:** clearest for one short, non-reused rule; weak for shared composition and ownership.
- **Pure function/predicate:** lightweight and composable; may lack stable identity, explanation, serialization, or query metadata.
- **Policy/rules engine:** supports managed rule languages and governance; adds operational, semantic, and security complexity.
- **Decision table/DMN:** makes finite business combinations reviewable; may be awkward for rich graph/state logic.
- **Query Object/criteria API:** owns retrieval shape and backend query semantics; may mix projection/order/page with domain truth.
- **Validation result:** accumulates path-specific violations; better than Boolean Specification when diagnostics are primary.
- **Domain method:** keeps invariant close to aggregate; preferable when rule belongs to one object and is not independently composed.
- **Strategy:** selects an algorithm producing a result; Specification classifies whether a proposition holds.

Specification is strongest as a small domain predicate algebra with explicit adapters, not as a universal distributed policy language.

## Failure Modes and Misconceptions

- **“Any lambda is a specification.”** Without domain name/contract it is only an anonymous predicate.
- **“Composition preserves meaning automatically.”** Effects, errors, unknown, time, and order can break Boolean laws.
- **“False means every non-success.”** It must not erase unavailable fact, malformed input, policy error, or denial reason.
- **“One object runs in memory and SQL.”** Only a restricted, verified semantic intersection can be translated honestly.
- **“Parameterized means safe.”** It reduces value injection, not costly queries, unauthorized fields, or missing tenant scope.
- **“Eligibility permits action.”** Authorization and transactional revalidation remain separate.
- **“A true check stays true.”** State, clock, policy, and external facts can change after evaluation.
- **“Explanations are harmless.”** Rule thresholds and evaluated attributes can disclose sensitive information.
- **“More generic is more reusable.”** Field/operator bags erase domain language and enable invalid combinations.
- **“Passing examples prove the rule.”** Examples establish finite traces, not completeness, legality, fairness, or safety.

## Worked Examples

### Example 1

`PremiumCustomer` means active AND lifetime spend at least 10,000. Two named leaves preserve vocabulary and boundary tests. **Conclusion:** Compose domain propositions, not field bags.

### Example 2

An AND composite's left leaf is false, so an expensive pure right leaf is skipped under the documented in-memory evaluator. **Conclusion:** Short-circuiting may optimize cost but cannot make an unsafe leaf valid.

### Example 3

Policy facts are unavailable; the evaluator returns indeterminate. Applying ordinary NOT would yield true if indeterminate were collapsed to false. **Conclusion:** Authorization needs a decision algebra and fail-safe combination table.

### Example 4

Application comparison lowercases Unicode differently from the database collation, producing different customer matches. **Conclusion:** Differential-test the target backend's actual semantics.

### Example 5

Only `country=SE` translates; a risk model remains in memory. The coarse query includes every possible full match and returns a bounded candidate set. **Conclusion:** Hybrid pushdown needs an implication argument and resource bounds.

### Example 6

A client sends 2,000 nested OR nodes over sensitive fields. Parser depth/node/field allowlists and cost budget reject it before planning. **Conclusion:** Rule-shaped input is an untrusted language.

### Example 7

`OrderCanShip` was true at version 7, but another transaction consumes inventory before dispatch. The command compares/rechecks version 7. **Conclusion:** Classification does not reserve state.

### Example 8

A reason tree contains full medical condition codes and fraud thresholds. Audience-specific redaction replaces operands with stable reason codes. **Conclusion:** Explainability requires disclosure design.

### Example 9

An empty conjunction is used to build optional filters and evaluates true; an empty disjunction evaluates false. Tests lock these identities. **Conclusion:** Variadic composite edge cases need explicit algebra.

### Example 10

A clinical eligibility specification matches a fixture set. Named clinical, legal, fairness, safety, and quality reviewers have not assessed the source criteria. **Conclusion:** Pattern and test evidence do not establish high-stakes fitness.

## Cross-Program Connections

- **Programming Languages and Semantics:** predicates, algebraic data types, effects, and evaluation order define the rule algebra.
- **Functional Programming:** pure functions, immutable composition, folds, and property laws offer a lightweight encoding.
- **Theory of Programming:** implication, equivalence, refinement, and proof obligations formalize subsumption and pushdown.
- **Software Design and Domain Modeling:** ubiquitous language, aggregates, value objects, and invariants determine rule ownership.
- **Database Systems and Engineering:** NULL, collation, indexes, joins, query planning, isolation, and snapshots constrain translation.
- **Security Engineering:** policy decisions, trusted attributes, fail-safe defaults, tenant enforcement, and information disclosure bound use.
- **API Engineering:** versioned filter ASTs, schema validation, depth limits, and compatibility expose safe external subsets.
- **Testing and Quality Engineering:** truth tables, boundaries, property, differential, mutation, fault, and historical replay tests provide evidence.
- **Data and AI Engineering:** model-backed predicates require versioned features, calibration, drift, uncertainty, and governance.
- **Distributed Systems:** stale facts, partial failure, policy versions, retries, and consistency prevent naive global truth claims.

## References

1. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003, ISBN 978-0-321-12521-7. Defines Specification as a domain pattern for selection, validation, and construction.
2. Eric Evans and Martin Fowler, [“Specifications”](https://martinfowler.com/apsupp/spec.pdf), 1997. Original pattern paper covering composite specifications and subsumption.
3. Erich Gamma et al., *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1994, ISBN 978-0-201-63361-0. Composite foundation for tree-structured rule composition.
4. Barbara Liskov and Jeannette Wing, [“A Behavioral Notion of Subtyping”](https://doi.org/10.1145/197320.197383), *ACM TOPLAS* 16(6), 1994. Contract foundation for interchangeable specification implementations.
5. Jakarta EE, [Jakarta Persistence 3.2 Specification, Criteria API](https://jakarta.ee/specifications/persistence/3.2/jakarta-persistence-spec-3.2.html), accessed 2026-08-28. Defines object-based criteria query construction and typed/string-based metamodel forms.
6. PostgreSQL Global Development Group, [Comparison Functions and Operators](https://www.postgresql.org/docs/19/functions-comparison.html), PostgreSQL 19 documentation, accessed 2026-08-28. Documents NULL/unknown Boolean comparison behavior and explicit truth tests.
7. NIST, [Guide to Attribute Based Access Control (ABAC) Definition and Considerations](https://doi.org/10.6028/NIST.SP.800-162), Special Publication 800-162, updated 2019. Defines subject, object, operation, environment, policy, and attribute considerations.
8. OWASP Foundation, [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), accessed 2026-08-28. Provides deny-by-default, every-request validation, and authorization-testing guidance.

## Exercises

### Exercise 1

Trace the executable example, derive the exact Boolean results, and state which algebraic and production claims it does not prove.

### Exercise 2

Design an explanatory four-outcome specification algebra for shipment eligibility with unavailable facts and evaluate representative AND, OR, and NOT cases.

### Exercise 3

Design a safe versioned external filter and translator for a multi-tenant order repository.

### Exercise 4

Plan evidence that an in-memory specification and PostgreSQL translation agree over their supported semantic subset.

### Exercise 5

Review a high-stakes model-backed specification without claiming clinical, legal, fairness, safety, or regulatory correctness.

## Answers to the Exercises

### Answer 1

Ada is active and 140 is at least 100, so AND is true. Bea has 220 spend but active is false, so short-circuit AND is false. Cy is active but 80 is below 100, so false. The eligible list is exactly Ada. For Bea, Active returns false and its total Boolean negation returns true.

This finite execution demonstrates named leaves, immutable-by-convention composition, deterministic two-valued AND/NOT, and exact output under one Python runtime. It does not prove arbitrary candidate validity, concurrency/freshness, Boolean laws under effects/errors, database translation/parity, query performance, authorization, or domain-policy correctness.

### Answer 2

Define outcomes `match`, `no_match`, `indeterminate(reason)`, and `error(reason)`, with bounded evidence and one facts/policy version. For AND: any no-match yields no-match if evaluating it is itself safe; all match yields match; otherwise indeterminate/error propagates under the documented precedence. For OR: any match yields match; all no-match yields no-match; otherwise indeterminate/error propagates. NOT swaps match/no-match but preserves indeterminate/error.

For shipment, `InventoryAvailable AND AddressServiceable AND NotEmbargoed` matches only with all affirmative facts. Zero stock yields no-match; unavailable inventory yields indeterminate; malformed address yields error; unknown embargo status remains indeterminate rather than becoming permitted. Capture one facts snapshot, reason codes, evaluated/skipped nodes, rule version, and redacted evidence. The dispatch command rechecks state transactionally before reserving inventory.

### Answer 3

Define data-only schema `{version:1, op:"and", args:[...]}` with leaves such as `{field:"status", op:"eq", value:"paid"}`. Allowlists expose only public typed filter fields and operations; the parser caps bytes, depth, nodes, list length, string length, numeric range, and time range, and rejects duplicate/unknown members and unsupported versions. It never accepts code, class names, raw SQL, arbitrary paths, regex without controls, projection, tenant, or authorization fields.

The server injects authenticated tenant/resource authorization independently, normalizes typed values, builds a parameterized criteria AST, bounds joins/result/page/cost/time, and reports unsupported/too-expensive filters. Test injection strings, forbidden fields, missing tenant constraints, wrong grouping, NULL, Unicode/collation, decimals, timestamps, huge/deep trees, costly disjunctions, schema skew, and access-control bypass. Log only bounded structural metadata.

### Answer 4

Specify the shared subset: candidate fields/validity, two- or three-valued null policy, Unicode normalization/collation, exact decimal scale/rounding, timestamp instant/time-zone boundaries, enum/version behavior, relationship quantifiers, and unsupported operations. Build boundary and generated fixtures including null/missing, empty, case/Unicode, decimal endpoints, DST transitions, duplicates, joins with zero/many rows, and tenant partitions.

Evaluate the same immutable fixtures using in-memory rules and a real supported PostgreSQL version, comparing candidate IDs and richer outcomes—not merely generated SQL. Mutation-test operators/grouping/null predicates/tenant injection, capture engine/schema/collation/time-zone versions, examine plans and resource limits, and test transactional snapshot assumptions. Differences block translation or require an explicit semantic adapter; a single passing sample is not equivalence proof.

### Answer 5

Define the decision purpose, population, candidate action, harms, source authority, exclusions, uncertainty, protected attributes/proxies, time horizon, operational context, override/appeal, and exact claim. Freeze/version model, features, preprocessing, thresholds, policy wrapper, facts, and explanation mapping. Distinguish model unavailable, missing feature, out-of-distribution input, no-match, denial, and evaluator error; fail safely for the consequence.

Evidence requires source-rule traceability, representative and subgroup performance with uncertainty, calibration/discrimination and error-cost analysis, external/temporal/site validation where applicable, data quality/leakage/drift tests, adversarial/privacy/security review, human-factors/workflow trials, accessibility, monitoring, incident/rollback, and applicable legal/regulatory quality records. Named domain/clinical, statistics/ML, fairness, safety, security/privacy, legal/regulatory, quality, human-factors, and operations reviewers approve. Specification structure, code execution, and fixture parity establish no high-stakes suitability by themselves.
