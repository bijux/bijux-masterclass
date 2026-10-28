---
module_id: SEPAT-049
program: Software Engineering: Patterns
level: 1
module_number: 49
title: Object Mother and Test Data Builder
status: complete
last_verified: 2026-08-28
---

# Object Mother and Test Data Builder

## One-Page Review

### Governing question

How can tests construct valid, intention-revealing domain examples with minimal irrelevant setup while preserving fixture freshness, invariant ownership, deterministic values, independent variation, schema evolution, persistence realism, privacy, and failure diagnostics?

### Essential definitions

- A **test fixture** is all state required before exercising a test: objects, records, files, services, clocks, and configuration.
- An **Object Mother** is a test factory that returns familiar named examples or scenario starting points.
- A **Test Data Builder** accumulates explicit overrides over valid defaults and constructs a fresh test object.
- A **valid default** satisfies production construction invariants while remaining irrelevant to the behavior under test.
- A **salient value** is an input whose value matters to the test's claim and therefore should be visible in the test.
- A **fresh fixture** is constructed for one test and is not shared mutably across tests/runs.
- A **scenario builder** coordinates several related aggregate roots or external records under one bounded scenario vocabulary.
- An **invalid fixture** intentionally violates a boundary for validation/deserialization/migration tests and must be produced through an explicit narrow unsafe seam.
- A **fixture oracle leak** occurs when tests copy the production rule they should independently verify into the builder/default logic.

### Central model, mechanism, or theorem

Let production constructor (C:P\to D\cup Error), valid default parameters (p_0\in P), and finite overrides (\Delta). A builder computes

\[
B(p_0,\Delta)=C(override(p_0,\Delta)).
\]

For every ordinary build, production invariants should hold because (C), not duplicated test logic, validates construction. Fixture quality is not proven by validity alone: the test must expose every salient override, build fresh independent state, and avoid defaults that determine the assertion invisibly.

### Critical invariants

- Ordinary builders create fresh valid production objects through public production construction paths.
- Defaults are deterministic, minimal, domain-plausible, and irrelevant to the assertion; salient differences are explicit at the test call site.
- `build` snapshots/copies mutable inputs so later builder or fixture mutation cannot alter prior products or other tests.
- Builders/Mothers live in test-owned code, use domain language, and do not become production dependencies or a second invariant implementation.
- Identity, clock, randomness, locale, time zone, tenant, and external references are explicit or deterministically controlled.
- Invalid/corrupt/legacy fixtures use named constrained seams and cannot be selected accidentally by ordinary tests.
- Persistence/integration fixtures respect real schema constraints, transaction cleanup, isolation, and parallel namespaces.
- Fixture reuse improves readability only while failures still identify the exact data relevant to each tested claim.

### Common failures

Common failures include a `TestDataFactory` god object, one shared mutable default instance, random defaults without seeds or failure replay, current time inside builders, globally reused IDs, hidden locale/time zone, Mother methods with dozens of positional parameters, “valid” defaults that encode the expected answer, builders bypassing production constructors, builder validation copied from production, every new field breaking hundreds of tests, deep object graphs built for unit tests, mocks hidden inside Mothers, database fixtures shared across parallel tests, real production/customer data, and snapshots so large that the assertion's cause disappears.

### Compact example

`CustomerMother.standard()` and `.gold()` return fresh builders with valid deterministic defaults. One built standard customer remains standard after its builder is changed to silver, while the named gold scenario carries a 5,000-cent credit limit.

### Connections

[SEPAT-048](048-policy-object.md) makes governed decisions testable; [SEPAT-050](../ROADMAP.md) diagnoses pattern overuse. Test-data patterns connect to [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), and [Database Engineering](../../18-database-engineering/ROADMAP.md).

## Governing Question

Which fixture details express the test's claim, which valid details can safely default, and what builder/Mother boundary creates a fresh deterministic example without hiding the production behavior the test is meant to challenge?

Use inline construction while it is clear. Introduce a Builder when constructor noise or repeated graph setup obscures intent; introduce an Object Mother when a small stable vocabulary of named examples genuinely helps the team reason.

## Why This Matters

Rich domain objects require IDs, values, relationships, histories, time, and configuration before a test reaches one behavior. Repeating all setup makes tests long and brittle; broad shared fixtures make them mysterious and coupled.

Test Data Builders let each test state only relevant variation over valid defaults. Object Mothers give recurring scenarios memorable names. Both can become harmful abstractions unless freshness, defaults, invariant ownership, and evolution are continuously reviewed.

## Prerequisites and Retrieval

You should understand Arrange-Act-Assert, domain constructors/invariants, Builder, factories, immutability/copying, test isolation, deterministic clocks/randomness, and database transactions. Retrieve these facts:

1. Test code is production-quality code but serves diagnostic and evidence goals rather than runtime delivery.
2. Shared mutable fixtures create order-dependent and parallel-test failures.
3. Production constructors/factories should remain the authoritative invariant boundary.
4. Random data without recorded seeds/shrinks is difficult to reproduce.
5. Persistence tests need real constraint/transaction semantics; in-memory objects cannot substitute for all database evidence.
6. A value that influences the expected outcome should normally be visible in the test.

## Learning Objectives

After completing this module, you should be able to:

- choose between inline setup, Object Mother, Test Data Builder, scenario factory, and generated data;
- design valid deterministic defaults and domain-named overrides;
- preserve freshness and copy/immutability across builder reuse;
- keep production construction/invariants authoritative;
- create explicit invalid, temporal, randomized, and persisted fixtures safely;
- evolve builders without hiding broad semantic changes;
- diagnose fixture coupling, mystery guests, overspecification, and false realism;
- review test-data evidence in high-stakes domains without overstating it.

## Core Exposition

### Start with the assertion's data dependency

List values that can change the observed result. Put those salient values directly in the test name/setup. Everything else may use a well-documented valid default only if changing it within its valid equivalence class cannot change the claim.

This discipline prevents a default tier, date, tenant, or status from becoming a hidden premise.

### Prefer inline setup while readable

For a value with three fields, direct construction may be clearest. A builder adds navigation and another API to learn. Extract when multiple tests repeat noisy valid details or constructor evolution obscures intent.

Do not measure quality by line count alone. Five explicit lines can diagnose a failure better than one opaque Mother call.

### Design valid-by-default builders

`CustomerBuilder().build()` should create a valid ordinary customer. Defaults use stable IDs, fixed captured instants, explicit currency/locale, smallest plausible collections, and no external effects.

Choose defaults that are semantically neutral for common tests, but do not invent a “neutral” value where the domain has none. Require explicit input for fields that are always salient or security-sensitive.

### Speak domain language

Use `with_credit_limit`, `placed_at`, `for_tenant`, `containing_line`, or `closed_on`, not generic `setField`. Methods should reveal the domain variation and validate types at build time.

Avoid long positional Mother parameters. Return a builder or accept named overrides so the call site names each difference.

### Keep products fresh and independent

Each `build` creates a new product and copies/finalizes mutable collections. Reusing a builder can be allowed only if previous products cannot change and subsequent overrides are clear. A persistent/immutable builder returning a new builder per override is safer for concurrent reuse.

Never return the same mutable canned entity instance from a Mother. Shared immutable value fixtures are acceptable when identity is irrelevant and immutability is enforced.

### Let production code enforce invariants

Builders call public production constructors/factories/value objects. They assemble data; they do not duplicate minimum-age, currency, status-transition, or uniqueness logic.

If production construction is impossibly awkward, treat fixture pain as design feedback. Improve production factories/aggregate boundaries where appropriate instead of using reflection to bypass them.

### Keep Object Mothers small and memorable

Named scenarios such as `standard_customer`, `gold_customer`, or `order_awaiting_payment` help only when their semantics are stable and familiar. Implement Mothers by composing builders, not by maintaining a separate graph-construction framework.

Delete near-duplicate persona methods. A Mother catalog with `customer17`, `valid2`, and `almostGoldButInactive` has lost its vocabulary.

### Build invalid data through explicit seams

Ordinary domain behavior tests should not create impossible objects. Parser/migration/validation/security tests may need malformed bytes, legacy rows, missing fields, corrupt checksums, or invariant-violating persistence state.

Name the unsafe producer after the boundary: `MalformedCustomerJson`, `LegacyRowV1`, or `CorruptRecordFixture`. Scope it to those tests, document which invariant is broken, and prevent it from leaking into general Mothers.

### Control identity and uniqueness

Default IDs that collide are fine for pure isolated unit tests but dangerous in shared/persisted contexts. Use a per-test deterministic namespace/counter derived from a test-run/test-case ID. Record generated values in failure output.

Do not derive security/tenant identities from mutable global counters. Integration fixtures include explicit tenant/user/authority relationships and exercise authorization independently.

### Control time

Inject a test clock or require an explicit fixed instant. Relative helpers such as `expired_two_days_ago(clock)` are meaningful only when one clock instant/time zone/calendar is captured.

Test inclusive endpoints, DST, leap days/seconds where relevant, and historical policy/calendar versions. A builder calling wall-clock now can make a test fail at midnight or after policy changes.

### Control randomness

Use explicit examples for named boundaries and property-based generators for broad exploration. Generators produce valid data by construction, record seed and minimized counterexample, and bound size/depth.

Do not fill irrelevant defaults with faker randomness. It creates noise without systematic coverage. If randomized uniqueness is needed, seed it per test and print/replay the seed.

### Separate objects from collaborations

Builders construct state/value/entity inputs. Test doubles define interactions with repositories, clocks, gateways, and publishers. A Mother that silently installs permissive authorization or always-successful payment mocks hides essential behavior.

Expose collaborators in the test arrangement and use narrow fakes/stubs/spies according to the claim. Do not let data helpers configure the entire application container.

### Build aggregate-sized graphs

Provide builders for aggregate roots and important value objects, not every internal class. Default children should be minimal. Scenario builders coordinate multiple aggregates only when the test is genuinely at integration/workflow scope.

Deep universal graphs slow tests, couple unrelated modules, and create a second object model. Split by bounded context and layer.

### Persist through realistic adapters

Unit-test builders return domain objects. Integration fixture writers translate via production repositories/API or a controlled database fixture adapter that respects schema constraints, defaults, triggers, generated keys, tenant partitioning, and transactions.

Direct inserts are useful to target storage edge cases but can bypass production behavior; label the evidence. Use per-test transaction/schema/database/key namespace and reliable cleanup for parallel execution.

### Evolve with production schemas

When a new required field appears, decide whether it is globally irrelevant and has one stable default. If it changes semantics, make affected tests choose explicitly instead of updating one Mother and silently changing hundreds of premises.

Compile/test failures are useful migration signals. Version external serialized fixture files and migrate or retain compatibility fixtures intentionally.

### Avoid expectation coupling

Do not compute expected result with the same policy/algorithm used by production. Builders may calculate structural derivatives needed for validity, but test oracles should come from independently derived constants, models, properties, or reference implementations.

A Mother named `customer_who_gets_discount` can encode the answer and make a circular test. Name input state, not expected output, unless it is a stable domain persona independently specified.

### Optimize diagnostics

On failure, render the salient builder overrides, final normalized values, seed, clock, schema/policy version, and fixture IDs—redacted as needed. Avoid dumping entire graphs or secrets.

Keep builders local to the tests that own them until real reuse appears. Broad central libraries increase the blast radius of every change and make dependency ownership unclear.

## Definitions and Notation

Let production parameter domain (P), valid domain objects (D), public constructor (C:P\to D\cup Error), defaults (p_0), and finite override map (\Delta). Builder operation is

\[
B(\Delta)=C(p_0\oplus\Delta).
\]

Freshness requires separate builds (d_1,d_2) not share mutable owned state. For every field (s) salient to assertion (A), test setup should expose (s) rather than rely on (p_0[s]). This is a review discipline, not a theorem automatically enforced by a builder API.

## Mechanisms, Invariants, or Proof Structure

### Test-data design procedure

1. Identify the test claim and every salient input, boundary, version, and collaborator.
2. Keep simple fixtures inline; extract only repeated irrelevant construction noise.
3. Define minimal deterministic valid defaults through production constructors.
4. Add domain-named overrides and copy/snapshot mutable inputs at build.
5. Add a small Mother catalog only for stable familiar scenarios, composed from builders.
6. Separate invalid data, clocks/random generators, test doubles, and persistence adapters.
7. Enforce per-test identity/isolation, parallel cleanup, schema evolution, and redacted diagnostics.
8. Review whether defaults hide premises/oracles and whether helper scope still matches ownership.

### Executable finite model

The following Object Mother returns fresh builders. Building snapshots primitive state, so changing a reused builder afterward does not mutate the prior product. It demonstrates local independence only—not full domain validation, threads, persistence, clocks, randomness, or schema migration.

<!-- bijux-verify: {"id":"test-data-builders","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"standard=Ada:standard:0\ngold=Ada:gold:5000\nindependent=standard\n","stderr":""}} -->
```python
class Customer:
    def __init__(self, name, tier, credit_limit_cents):
        if tier not in ("standard", "silver", "gold"):
            raise ValueError("invalid tier")
        if credit_limit_cents < 0:
            raise ValueError("invalid credit limit")
        self.name = name
        self.tier = tier
        self.credit_limit_cents = credit_limit_cents


class CustomerBuilder:
    def __init__(self):
        self.name = "Ada"
        self.tier = "standard"
        self.credit_limit_cents = 0

    def with_name(self, name):
        self.name = name
        return self

    def with_tier(self, tier):
        self.tier = tier
        return self

    def with_credit_limit(self, cents):
        self.credit_limit_cents = cents
        return self

    def build(self):
        return Customer(self.name, self.tier, self.credit_limit_cents)


class CustomerMother:
    @staticmethod
    def standard():
        return CustomerBuilder()

    @staticmethod
    def gold():
        return CustomerBuilder().with_tier("gold").with_credit_limit(5000)


builder = CustomerMother.standard()
standard = builder.build()
gold = CustomerMother.gold().build()
builder.with_tier("silver")
print("standard=" + standard.name + ":" + standard.tier + ":" + str(standard.credit_limit_cents))
print("gold=" + gold.name + ":" + gold.tier + ":" + str(gold.credit_limit_cents))
print("independent=" + standard.tier)
```

In production, immutable values would further prevent product mutation. The example deliberately keeps the Builder test-owned and delegates tier/credit validation to `Customer`.

## Alternatives and Trade-Offs

- **Inline setup:** most explicit and local; duplicates noise for rich repeated construction.
- **Creation/helper method:** good for one test class or one small recurring object; less flexible than a fluent builder.
- **Object Mother:** shared named personas speed recognition; changes couple many tests to canned details.
- **Test Data Builder:** explicit variation over defaults; adds an API and can hide premises.
- **Factory/fixture factory:** straightforward parameterized construction; long argument lists reduce readability.
- **Property-based generator:** broad valid/adversarial exploration with shrinking; less narrative than named examples.
- **Parameterized/data-driven rows:** excellent for compact tables; awkward for rich object graphs.
- **Scenario/DSL:** expressive multi-object workflows; risks duplicating production orchestration and becoming a framework.
- **Production factory:** may be reusable when its API fits; test-only convenience must not pollute production.
- **Captured/prebuilt data:** realistic regressions/compatibility; needs provenance, privacy, versioning, and isolation.

Combine patterns by evidence need: explicit named boundaries plus generated valid spaces, not one universal fixture system.

## Failure Modes and Misconceptions

- **“All defaults should be realistic.”** Minimal deterministic validity is usually more diagnostic than a giant typical graph.
- **“Builders eliminate test maintenance.”** They localize irrelevant constructor changes but should expose semantic changes.
- **“A Mother object is shared.”** The factory may be shared; ordinary mutable products must be fresh.
- **“Invalid objects need reflection.”** Prefer malformed boundary representations or explicit constrained unsafe seams.
- **“Random equals comprehensive.”** Coverage needs a generator model, seeds, shrinking, and boundary examples.
- **“One builder per class is modular.”** Aggregate/bounded-context ownership is usually the durable test boundary.
- **“Integration fixtures should use only public APIs.”** Direct storage setup can target schema behavior if evidence limits are clear.
- **“Passing with production data is realistic.”** It risks privacy, nondeterminism, drift, and irreproducibility.
- **“The helper can calculate expected values.”** Shared algorithms create circular oracles.
- **“Fixture validity proves behavior.”** It proves construction for that example, not the tested rule or system correctness.

## Worked Examples

### Example 1

A tax test hides currency in a default, and changing default USD to EUR flips the result. Currency becomes an explicit salient override. **Conclusion:** Defaults must not hide assertion premises.

### Example 2

One Mother returns the same mutable customer to every test. A status mutation makes results order-dependent. Fresh builders eliminate sharing. **Conclusion:** Factory reuse is not product reuse.

### Example 3

Builder copies production age-validation code and both share the same defect. Calling the production constructor restores one invariant owner. **Conclusion:** Builders assemble; production validates.

### Example 4

A parser test needs a missing required JSON field. It uses `MalformedCustomerJson.missing_name`, not an impossible domain Customer. **Conclusion:** Break invariants at the boundary under test.

### Example 5

Random names and dates change every run but exercise no meaningful partition. Fixed defaults plus property generators with seeds improve evidence. **Conclusion:** Random noise is not generative testing.

### Example 6

A payment Mother installs an always-success gateway, hiding decline behavior. The test arranges a visible stub separately. **Conclusion:** Separate state fixtures from collaboration behavior.

### Example 7

Parallel database tests use ID `1` and delete each other's rows. Per-test tenant/schema/key namespaces restore isolation. **Conclusion:** Persistence identity is part of fixture lifecycle.

### Example 8

A new required compliance category is defaulted globally, silently changing every test's meaning. A compile failure forces explicit migration. **Conclusion:** Semantic schema changes should stay visible.

### Example 9

Expected discount is computed by the same policy used by the system. A hard-coded independently derived boundary table catches a mutation. **Conclusion:** Do not build the oracle with the subject algorithm.

### Example 10

De-identified clinical records pass a workflow test but represent no validated population or safety outcome. **Conclusion:** Fixture realism is not clinical validity.

## Cross-Program Connections

- **Object-Oriented Programming:** Builder/factory, encapsulation, immutability, copying, identity, and aliasing shape fixtures.
- **Functional Programming:** pure generators, immutable values, persistent updates, and property/shrinking models improve data creation.
- **Software Design and Domain Modeling:** aggregates, constructors, invariants, ubiquitous language, and contexts determine builder boundaries.
- **Testing and Quality Engineering:** fresh fixtures, tests as documentation, oracles, doubles, properties, mutations, and diagnostics define evidence.
- **Database Engineering:** constraints, generated IDs, transactions, cleanup, schemas, and isolation govern persisted fixtures.
- **Concurrency Engineering:** shared state, parallel namespaces, deterministic schedulers, and teardown races constrain tests.
- **Security Engineering:** tenant/authority facts, synthetic data, secret handling, privacy, and unsafe fixture seams require controls.
- **Data Engineering:** dataset provenance, schema/version, quality, lineage, sampling, and deterministic snapshots govern data fixtures.
- **API and Service Engineering:** versioned payloads, compatibility, malformed cases, and contract fixtures test boundaries.
- **Safety and High-Assurance Engineering:** representative cases, traceability, independent oracles, and domain review exceed convenient construction.

## References

1. Martin Fowler, [Object Mother](https://martinfowler.com/bliki/ObjectMother.html), 2006, accessed 2026-08-28. Defines Object Mother as a factory for familiar standard test fixtures and notes coupling costs.
2. Peter Schuh and Stephanie Punke, [“ObjectMother: Easing Test Object Creation in XP”](https://citeseerx.ist.psu.edu/document?doi=a55fa574c23f04c86b3472c95cd68d5a3080d8da&repid=rep1&type=pdf), XP Universe 2001. Original pattern treatment of constructing and tailoring test objects.
3. Steve Freeman and Nat Pryce, *Growing Object-Oriented Software, Guided by Tests*, Addison-Wesley, 2009, ISBN 978-0-321-50362-6. Develops Test Data Builders and expressive test-domain construction.
4. Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, ISBN 978-0-13-149505-0. Defines fixture setup, fresh/shared fixtures, creation methods, test smells, and diagnostic patterns.
5. Gerard Meszaros, [“A Pattern Language for Setting up XUnit Test Fixtures”](https://hillside.net/plop/2004/papers/gmeszaros0/PLoP2004_gmeszaros0_0.htm), PLoP 2004. Primary pattern language for fixture strategy and construction.
6. Kent Beck, *Test-Driven Development: By Example*, Addison-Wesley, 2002, ISBN 978-0-321-14653-3. Provides small explicit examples and test-first design discipline.
7. David Saff and Michael D. Ernst, [“An Experimental Evaluation of Continuous Testing During Development”](https://doi.org/10.1145/1028976.1029003), ISSTA 2004. Empirical foundation for fast deterministic developer feedback.
8. Claessen and Hughes, [“QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs”](https://doi.org/10.1145/351240.351266), ICFP 2000. Primary source for property-based generation and counterexample shrinking.

## Exercises

### Exercise 1

Trace the executable Mother/Builder example and state exactly which freshness, validity, copying, and test-evidence claims it does and does not establish.

### Exercise 2

Design a valid-by-default order Test Data Builder and a small Object Mother vocabulary without hiding pricing premises.

### Exercise 3

Design explicit invalid, randomized, time-dependent, and versioned fixture paths for an API parser and domain model.

### Exercise 4

Plan migration of a broad shared Mother library after a semantically significant required field is added.

### Exercise 5

Review high-stakes synthetic or captured test data without claiming population representativeness, clinical validity, safety, or regulatory fitness.

## Answers to the Exercises

### Answer 1

`standard()` creates a new builder with Ada/standard/0; `build` calls Customer, whose checks accept it. `gold()` creates a separate builder, overrides tier then credit, and builds Ada/gold/5000. Mutating the first builder's tier to silver changes its field but not the already constructed Customer's primitive `tier`, so printed independent remains standard.

The run establishes two fresh builders/products by construction, valid tier/nonnegative-credit paths, deterministic defaults, named overrides, and post-build independence for immutable primitive references. It does not prove deep copying of collections, immutable products, concurrent builder reuse, all invalid boundaries, IDs/time/randomness, persistence isolation, schema evolution, absence of hidden salient defaults, or correctness of any system behavior tested with these objects.

### Answer 2

`OrderBuilder` defaults to deterministic order/customer IDs, one fixed currency, captured order instant, draft status, and an empty or one minimal line only if that is universally valid. It exposes domain methods `for_customer`, `in_currency`, `placed_at`, `containing(sku, quantity, unit_price)`, and `with_shipping_destination`; `build` creates production Money/Line/Order through public constructors and copies line values. Price, quantity, currency, discount eligibility, tax jurisdiction, and time must be explicit in pricing tests.

`OrderMother.empty_draft()`, `single_line_draft()`, and `awaiting_payment()` return fresh builders/scenario values with documented stable semantics; avoid outcome names such as `discounted_order`. Payment/shipping collaborators remain visible test doubles. Test builder defaults/build independence/collection copies and production rejection, but do not duplicate production rules. Property generators compose valid line/value generators with fixed seeds; persistence adapters allocate per-test tenant/key namespace.

### Answer 3

Keep four surfaces. Ordinary `CustomerBuilder` produces only valid domain objects through production constructors. Boundary fixtures produce versioned bytes/JSON such as missing-name, duplicate key, wrong type, huge depth/string, unknown field/version, invalid Unicode, and corrupt signature without first constructing a domain object. A test-only unsafe persistence fixture can insert specifically documented legacy/corrupt rows through a constrained adapter and isolated schema, never general Mothers.

Generators create valid facts by construction with explicit seed/size, record/shrink counterexamples, and provide separate invalid generators per constraint. Time-dependent Mothers require an injected fixed clock/time zone/calendar and name endpoint cases; no wall clock. Serialized golden fixtures carry schema/policy version, provenance, expected compatibility result, non-sensitive synthetic values, and migration ownership. Tests verify determinism, replay, cleanup, redaction, compatibility matrix, and that unsafe paths cannot leak into ordinary domain tests.

### Answer 4

Classify the new field: structural irrelevant default, domain-semantic input, security/tenant input, or versioned compatibility data. Search every builder/Mother consumer and identify tests whose assertion can depend on it. Do not set one global value until this analysis. Add production construction first so compile failures reveal affected paths; update only truly irrelevant local builders with a documented default and make semantic/security tests choose explicitly.

Split the god Mother by bounded context/aggregate ownership, replace near-duplicate personas with builders, and keep compatibility Mothers for old serialized schema under versioned names. Run old/new fixture differential inventory, mutation tests for hidden dependence, randomized test order/parallel isolation, schema/API/persistence compatibility, and diagnostic review. Commit migrations in coherent owner-scoped changes, measure use before deleting legacy helpers, and provide rollback only if runtime fixture infrastructure is involved; ordinary test-code changes should remain reviewable and deterministic.

### Answer 5

Define test purpose, target population/system configurations, outcomes/hazards, data source or synthesis model, inclusion/exclusion, temporal/site/device coverage, protected groups/proxies, privacy/consent/retention, missingness, labeling authority, and exact claim. Version generator/captured dataset, schema, preprocessing, code lists/units, policy/model/config, seeds, and expected/reference outputs. Keep synthetic and captured data clearly labeled and prevent re-identification or production-secret leakage.

Evidence requires domain/statistical sampling review, distribution and subgroup/rare-event coverage with uncertainty, external/temporal/site representativeness where claimed, provenance/lineage/quality and label agreement, boundary/adversarial/out-of-distribution cases, independent reference/oracles, privacy/security review, end-to-end device/workflow/human-factors trials, fault/resource tests, monitoring/incident/rollback, and applicable quality/regulatory records. Named domain/clinical, statistics, fairness, safety, security/privacy, legal/regulatory, data quality, human-factors, and operations reviewers approve. Convenient valid fixtures and passing tests establish no population, clinical, safety, or regulatory fitness.
