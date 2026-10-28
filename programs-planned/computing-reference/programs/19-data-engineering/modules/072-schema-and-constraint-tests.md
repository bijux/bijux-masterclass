---
module_id: DE-072
program: Data Engineering
level: 2
module_number: 72
title: Schema and Constraint Tests
status: complete
last_verified: 2026-09-03
---

# Schema and Constraint Tests

## One-Page Review

### Governing question

How can a data platform prove that each published dataset conforms to an explicit structural and semantic contract across formats, engines, schema versions, historical data, and write paths—without mistaking parser success, registry compatibility, sampled checks, or unenforced declarations for complete correctness?

### Essential definitions

- A **schema** specifies the structural vocabulary of data: fields, identities/names, types, nesting, repetition, nullability or presence, defaults, and sometimes openness to unknown fields.
- A **constraint** is a predicate or relationship that admissible data must satisfy for a declared scope.
- A **schema test** compares an instance or dataset's observed structure with an expected schema and dialect/version.
- A **constraint test** evaluates a declared predicate over applicable values, records, keys, relationships, groups, windows, or dataset aggregates.
- An **enforced constraint** participates in the write transaction and rejects violating state; an **observational test** reports on a version after or outside the write.
- **Writer schema** describes encoded data; **reader schema** describes the interpretation requested by a consumer.
- **Backward compatibility** usually means new readers can consume old data; **forward compatibility** means old readers can consume new data; **full compatibility** requires both, under one precisely named system's semantics.
- **Presence** distinguishes whether a value was supplied; it is not identical to null, zero, empty, or a default materialized by a reader.
- An **open schema** permits unspecified members; a **closed schema** rejects them in the applicable scope.
- A **primary/candidate key constraint** requires a chosen field tuple to be present and unique at a declared entity/version grain.
- A **referential constraint** requires a non-null foreign-key tuple to resolve in a pinned parent population under defined temporal semantics.
- A **cross-field constraint** relates fields within a record; a **cross-row/aggregate constraint** relates multiple records or totals.
- A **transition constraint** limits how an entity may change between ordered states, not merely whether each isolated state looks valid.
- A **test suite version** is the immutable set of schemas, rules, references, parameters, engine behavior, and severities used for one evaluation.
- **Evaluation coverage** records what fraction of the intended population the test actually evaluated and which parts were unknown.

### Central model, mechanism, or theorem

Let contract version $C_k=(S_k,R_k,P_k)$ contain schema $S_k$, rules $R_k$, and evaluation policy $P_k$. For pinned dataset version $D_v$, a suite passes only when schema conformance succeeds, every critical applicable rule passes, and required evaluation coverage is complete:

$$
Pass(D_v,C_k)\iff SchemaOK(D_v,S_k)\land
\bigwedge_{r\in R_k^{critical}} RuleOK(r,D_v)\land Coverage(D_v,C_k)=1.
$$

This proves conformance only to the declared, correctly implemented suite over $D_v$. It cannot prove an unspecified property, correspondence to reality, or future compatibility. For rule $r$ with applicable population $U_r$,

$$
RuleOK(r,D_v)\iff \forall x\in U_r:P_r(x),
$$

provided the entire $U_r$ was evaluated. Sampled results require statistical claims, not universal ones.

### Critical invariants

- Every schema declares its language/dialect, identifier, version, canonical digest, ownership, and effective scope.
- Field identity, name, type, nesting, presence/nullability, default, logical meaning, unit, and constraints remain distinct metadata.
- Reader/writer compatibility is tested in both required directions with actual encoders/decoders and representative boundary values.
- Adding a default does not prove producers supplied a value; presence and provenance remain observable where required.
- Unknown-field policy is explicit at each nested scope; open and closed behavior is not inferred from a tool default.
- Constraint null/unknown semantics are deliberate; a SQL `CHECK` that evaluates unknown may pass unless `NOT NULL` is separate.
- Keys define entity and temporal grain before uniqueness is measured; duplicate groups and excess rows are both reported.
- Referential tests pin both child and parent versions and define null, late parent, effective-time, and deletion behavior.
- Cross-field, cross-row, aggregate, and transition rules identify their exact grain, ordering, tolerance, and reference state.
- Enforced, declared-but-unenforced, and observational constraints are labeled accurately for every write path.
- Historical/backfill data is validated when a new rule is activated unless the contract explicitly scopes only future writes.
- Test execution failure, partial scans, unsupported keywords, or stale reference data never become a pass.
- Results bind dataset and suite versions, engine/library, counts, coverage, failures or protected digests, and gate action.
- Schema/rule evolution is canaried across the whole producer-consumer fleet and uses staged compatibility windows.
- Passing tests are evidence of specified conformance, not completeness, accuracy, business fitness, or absence of other defects.

### Common failures

Common failures include treating file parse as schema conformance; ignoring the schema dialect; validating only column names; relying on order where stable field IDs exist; confusing absent with null/default; assuming JSON Schema `format` always asserts; closing only the top-level object; calling registry compatibility semantic safety; testing a new reader but not old readers against new writes; reusing Protobuf field numbers; changing Avro defaults without resolution fixtures; expecting SQL `CHECK (x > 0)` to reject null; declaring a warehouse key that is not enforced; testing uniqueness at the wrong grain; comparing foreign keys to a moving parent; validating only new rows when old rows violate; sampling a rare critical rule; and reporting a crashed test job as green.

### Compact example

An orders contract requires exactly `order_id`, `customer_id`, `amount`, `status`, and `closed_at`; positive amounts; status in `{open, closed}`; `closed_at` present when closed; unique order IDs; and customer IDs present in pinned customer snapshot C17. Five rows match the physical schema. Row O3 has a negative amount and unknown customer, O4 lacks a required close timestamp, and O2 occurs twice. Structural conformance alone passes; row, key, and relationship tests fail. The suite therefore rejects publication with exact rule counts and dataset/contract versions.

### Connections

[DE-004](004-avro-protocol-buffers-and-schema-aware-serialization.md) establishes writer/reader serialization, [DE-008](008-schemas-nullability-and-type-fidelity.md) defines type and null semantics, [DE-036](036-merge-and-upsert-semantics.md) defines mutation keys, [DE-049](049-run-metadata-and-operational-state.md) identifies test executions, [DE-064](064-schema-evolution.md) handles stable table-field identities, and [DE-071](071-completeness-validity-accuracy-and-consistency.md) distinguishes quality dimensions. DE-073 adds source-to-target reconciliation; DE-074 adds temporal freshness.

## Governing Question

A schema is executable documentation, but “the schema passed” can mean many things. A parser may have accepted bytes. A registry may have judged two definitions compatible. A warehouse may expose the expected columns. A validator may have checked a sample. A database may have rejected a transaction. These observations have different scopes and strengths.

Constraints extend beyond shape. Amount must be positive, an order ID unique, a customer reference resolvable, line totals equal headers, and state changes follow allowed transitions. Some engines enforce these during writes; many analytical systems expose declarations without enforcement or rely on asynchronous tests.

Evolution makes correctness directional. A new reader may read old data while an old reader misinterprets new enum values. A wire-compatible numeric widening can still lose values in an older client. A newly required field can pass because a reader materializes a default even though producers never sent it.

The governing requirement is a layered, versioned suite whose evidence states precisely what was parsed, compared, enforced, scanned, and proven. Test authors must model nulls, identity, history, compatibility, and engine behavior, then integrate failures and unknowns into safe publication and remediation.

## Why This Matters

Schema drift often fails far from its source. A producer renames a field, one deserializer supplies a default, another reads null, a transformation casts silently, and a consumer discovers the problem days later. Early compatibility and instance tests shrink the fault domain.

Analytical constraints protect meaning that physical types cannot. An integer permits negative quantities; a timestamp type permits close-before-open; a string permits an unknown currency. Keys and relationships ensure rows form a coherent dataset rather than individually plausible fragments.

False assurance is especially dangerous. Some databases declare informational primary/foreign keys for optimization but do not enforce them. JSON Schema dialects distinguish annotations from assertions. SQL three-valued logic lets unknown satisfy many check expressions. A test framework may exclude nulls or cap failure output by default.

Tests also cost compute and delay. Full uniqueness or foreign-key scans are expensive at scale; exact enforcement can create write contention. Incremental tests reduce cost but require a proof that affected old/new relationships are covered. Risk and architecture decide placement, not a reflex to test everything everywhere.

Contracts are security artifacts. Failure rows may contain personal data, schemas reveal sensitive fields, and error messages can leak values. Evidence must be sufficient for diagnosis while minimized, access-controlled, encrypted, and retained appropriately.

## Prerequisites and Retrieval

Retrieve contract purpose: producer, consumers, business decisions, criticality, entity and event grain, keys, relationships, invariants, risk tolerance, publication policy, regulatory constraints, and accountable owners.

Retrieve physical formats: JSON Schema dialect/vocabularies, Avro/Protobuf definitions, Parquet/ORC logical types, database/table schema, field IDs/numbers, encodings, decimal precision/scale, timestamps/timezones, arrays/maps/unions, and canonical digests.

Retrieve compatibility semantics: registry mode and scope, writer/reader direction, transitive versus latest comparison, aliases, defaults, unknown fields, reserved identifiers, enum behavior, logical types, wire versus JSON/text form, and actual client versions.

Retrieve dataset state: table UUID/snapshot/version, partitions, row counts, schema ID, creation/evolution history, backfills, deleted/history rows, branches, late data, and all write paths including bulk load, streaming, SQL, APIs, and maintenance.

Retrieve rules: ID, description, dimension, subject/grain, expression, applicability, null/unknown behavior, tolerance, reference data/version, severity, owner, effective interval, historical scope, sampling/incremental method, and disposition.

Retrieve key semantics: canonicalization, null behavior, composite fields, entity versus event uniqueness, effective interval, late corrections, duplicate winner, and legitimate repeated occurrences.

Retrieve relationship semantics: child/parent keys, pinned versions, optionality, cardinality, effective-time join, late-parent window, soft deletion, tenant boundary, referential action, and allowed exceptions.

Retrieve execution: engine/library/version, supported keywords and SQL mode, scan/query plan, partitions and columns read, pushdown, sampling, timeout, permissions, result limits, retries, and failure-state mapping.

Retrieve lifecycle: local producer checks, registry admission, staging validation, write-time enforcement, post-commit tests, publication gate, quarantine, incident response, waiver, correction/backfill, and consumer notification.

Distinguish syntax from semantics; definition validity from instance validity; writer from reader schema; backward from forward compatibility; absent from null/default; physical type from logical type/unit; declaration from enforcement; current-row from transition constraint; zero violations from zero evaluated; schema compatibility from business compatibility; and conformance from accuracy.

Create a schema-and-constraint test contract:

| Concern | Required decision and evidence |
|---|---|
| Identity | Dataset UUID/version, schema ID/version/dialect/digest and suite version |
| Structure | Fields/IDs/types/nesting/presence/defaults/openness/logical annotations |
| Compatibility | Direction, transitivity, wire form, producer/consumer matrix and fixtures |
| Rules | Predicate, grain, applicability, null semantics, tolerance, reference and severity |
| Relationships | Key/uniqueness/FK/cardinality/temporal/aggregate/transition semantics |
| Execution | Engine/version, enforced versus observed, full/incremental/sample scope and coverage |
| Evidence | Counts, unknowns, protected failures/digests, input/reference versions and action |
| Lifecycle | Admission, canary, activation, historical validation, waiver, repair and retirement |

Write a falsifiable claim: “Snapshot S81 is evaluated by suite Q14 using JSON Schema 2020-12 assertion vocabulary J9 and SQL rules R31 on engine E6; exact nested schema/field identities match, old/new writer-reader fixtures pass the declared full-transitive window, all 48.2 million applicable rows and pinned reference P20 are scanned, critical not-null/domain/key/FK/cross-field/aggregate/transition rules have zero failures and zero unknowns, result artifacts bind digests and counts, and only the transactional write path enforces the subset labeled enforced.”

## Learning Objectives

After completing this module, you should be able to:

1. separate schema definition, instance conformance, compatibility, enforcement, and observational testing;
2. specify field identity, type, nesting, presence/nullability, defaults, logical meaning, and open/closed behavior;
3. test backward/forward compatibility with actual writer-reader matrices and boundary fixtures;
4. design value, cross-field, key, uniqueness, referential, aggregate, and transition constraints;
5. reason correctly about SQL null/unknown semantics and validator dialect options;
6. decide which constraints belong at producer, registry, transactional write, staging, or post-commit layers;
7. validate historical and incremental data with defensible scope and coverage;
8. version, canary, activate, waive, and retire schema/rule changes safely;
9. produce reproducible, privacy-aware results that distinguish violations from execution failure; and
10. explain exactly what a passing suite proves and what remains unproven.

## Core Exposition

### Build a layered contract

Use separate layers because each catches different defects. Container and parse checks establish readable bytes. Structural checks establish fields, types, nesting, presence, and annotations. Compatibility checks exercise old/new readers and writers. Row constraints establish value and cross-field rules. Dataset constraints establish keys, relationships, aggregates, and transitions. Operational checks establish scan coverage and correct gating.

A canonical schema record includes language/dialect, schema ID/version, canonical digest, field identities/numbers and names, types/logical types, cardinality/presence/nullability, defaults, aliases, deprecations, reserved identifiers, and unknown-member policy. Store it independently from one generated language class.

Nested schemas require nested policy. Closing the top-level JSON object does not necessarily close objects under arrays or referenced subschemas. Conversely, rejecting all unknown fields can make additive evolution impossible. Choose openness according to producer ownership, compatibility, typo risk, and forwarding requirements.

Order is rarely semantic for named records but can matter for tuples, CSV, positional inserts, or physical encodings. Test by stable identity where supported. A same-name field with a new Iceberg ID or reused Protobuf number is not the same field merely because display names match.

Logical annotations matter. Decimal precision/scale, UUID, date, local timestamp versus instant, timezone, duration, currency, and units must be tested beyond primitive storage. Cross-engine round trips expose silent truncation or timezone conversion.

### Treat presence, null, and defaults precisely

Presence asks whether the writer supplied a field. Null is an explicit value in systems that support it. Empty string/list, zero, false, unknown sentinel, and omitted field are distinct unless the contract deliberately normalizes them.

Defaults are contextual. In Avro, a reader default can fill a reader field missing from the writer schema and does not make the field optional when encoding. Protocol Buffers scalar presence depends on declaration and API; the default numeric value can be indistinguishable from absent without explicit presence. JSON Schema's `default` is generally annotation, not automatic mutation.

Test both decoded values and raw/presence metadata when the distinction affects business meaning. A completeness rule should not report source-provided merely because the reader constructed a default.

SQL constraints use three-valued logic. In PostgreSQL, a check is satisfied when its expression is true or null/unknown. `CHECK (amount > 0)` therefore needs `amount NOT NULL` if null is forbidden. Test true, false, and unknown cases explicitly in each target engine.

Nulls in unique and foreign-key constraints also vary by product and definition. Specify whether multiple null keys are allowed, whether composite partial null is permitted, and whether null references mean optional relationship or malformed data.

### Test compatibility as a matrix

Name direction from the data flow. Backward/forward terminology is used differently in casual conversation, so record concrete pairs: reader new with writer old, and reader old with writer new. “Full” means both under the chosen registry's comparison window, not all future programs.

Compatibility must cover the serialization form. Protocol Buffer binary changes differ from ProtoJSON/text behavior. Avro resolution depends on writer and reader schemas, aliases, defaults, type promotion, and data values. JSON Schema validates instances and does not itself supply a universal producer-consumer rollout protocol.

For each producer schema $W_i$, reader $R_j$, and fixture $x$,

$$
Compat(W_i,R_j,x)=Decode_{R_j}(Encode_{W_i}(x))\equiv_{contract}x.
$$

The equivalence is semantic, not merely “decoder returned.” Check values, presence, unknown preservation, precision, enums, maps, repeated fields, and reserialization.

Use fixtures at boundaries: min/max numbers, large widened values, unknown enums, removed fields, nested optional values, union branches, empty collections, Unicode, decimal extremes, timestamp transitions, duplicate map keys, and invalid legacy records. A compatible type change may still be lossy for particular values.

Compare against every supported historical version if policy is transitive. Latest-only checks can accept a sequence whose endpoints are incompatible. Test dormant and disaster-recovery clients before activation.

### Define row and dataset constraints

Value constraints include type, domain, range, pattern, length, precision, and reference membership. Cross-field constraints encode implications such as `status='closed'` requiring `closed_at`, or discount not exceeding price. Make applicability and null semantics explicit.

Define a key from entity/event grain. For key function $K$, uniqueness is

$$
\forall x,y\in D:K(x)=K(y)\Rightarrow x=y,
$$

after declared canonicalization and temporal scoping. Report duplicate keys, rows in duplicate groups, and excess rows because each answers a different operational question.

Referential integrity for child $D_c$ and parent $D_p$ is

$$
\forall x\in D_c:K_c(x)\ne NULL\Rightarrow K_c(x)\in K_p(D_p),
$$

under pinned versions and effective-time rules. A late parent may be temporarily allowed; soft-deleted parents and tenant boundaries need explicit handling.

Aggregate rules compare independently derived quantities: header equals lines, debits equal credits, count equals manifest control, probabilities sum within tolerance. Avoid recomputing both sides through the same buggy expression.

Transition rules compare ordered states: allowed status graph, monotonically increasing sequence, balance change equals transactions, immutable creation identity, or slowly changing dimension intervals do not overlap. Testing snapshots independently cannot detect an illegal but individually valid transition.

### Understand enforcement strength

Producer validation gives fast feedback but can be bypassed. Registry checks govern admitted schema definitions but not every instance or business predicate. Write-time database/table constraints can reject violations atomically but vary in supported/enforced semantics and may cost contention. Staging tests can quarantine before publication. Post-commit tests observe a committed version and require publication/fencing policy.

Maintain an enforcement matrix by rule and write path. PostgreSQL primary, unique, foreign-key, not-null, and check constraints have transactional semantics, but cross-row logic cannot safely be smuggled into immutable row checks. Delta Lake documents not-null/check enforcement and protocol implications. Other analytical warehouses may treat key declarations as informational. Retrieve rather than assume.

For observational tests, use a pinned version and publish only after the gate attaches a passing result to that exact version. If readers can access an unvalidated version, the architecture is monitor-after-publication, not prevention.

Constraint code must be deterministic for its declared inputs. Current time, mutable external tables, nondeterministic functions, or session-specific settings make historical results irreproducible. Pin reference data and parameters.

### Validate existing, incremental, and sampled data

Adding a rule to an existing table poses two questions: will future writes be checked, and do historical rows conform? Some systems validate all existing rows before activation; others allow not-valid/unvalidated constraints followed by a scan. Record state transitions and never label unvalidated state enforced for history.

Full scans provide universal evidence for deterministic predicates over the pinned scanned population, assuming correct implementation. Incremental tests must cover new/changed rows plus affected relationships. A changed parent can invalidate old children; a new duplicate can conflict with any historical key; a late event can alter an old window.

Use indexes, partition summaries, manifests, or maintained states only with proven soundness. A Bloom filter can accelerate candidates but false positives need exact resolution; a probabilistic structure with false negatives cannot prove zero violations.

Sampling is appropriate for exploration, expensive accuracy assessment, or noncritical monitoring, but it cannot prove a zero-tolerance universal constraint. Report sample design and uncertainty. Never sample primary-key uniqueness and then claim the table is unique.

Record coverage: intended partitions/rows/bytes versus scanned; pushdown and excluded states; unknown/error counts; reference freshness; and query plan. A test over an empty table may pass vacuously while a separate completeness rule should fail expected population.

### Evolve and operate test suites

Treat schemas and tests as code with domain review. Use stable rule IDs, ownership, descriptions, fixtures, counterexamples, severity, version/effective interval, and change rationale. Unit-test the rule itself against passing, failing, null, boundary, malformed, and engine-specific cases.

Use mutation tests where feasible: alter the predicate or inject known defects and ensure the suite fails. A test that never fails on a counterexample is not protecting the contract.

Roll out in stages: propose, compatibility/static check, run advisory on historical and recent data, inspect failures, repair or approve scoped exceptions, canary producers/consumers, enable gating/enforcement, then retire old versions after the compatibility window.

A waiver identifies rule, dataset/cohort, reason, approver, risk, compensating control, owner, and expiry. It changes disposition, not observed facts. Preserve the violation result.

Observe rule pass/fail/unknown counts, coverage, duration/cost, false-positive disputes, incidents caught/escaped, waiver age, schema drift, incompatible attempts, and time to repair. Delete obsolete rules only after consumers and historical interpretation no longer depend on them.

### Preserve evidence and respond safely

A result includes dataset UUID/version/digest, suite/schema/rule versions, engine/library and SQL mode, reference versions, timestamps, scope/coverage, success/failure/unknown/not-applicable counts, bounded protected examples or hashes, and final decision.

Do not store all violating rows in general logs. Use counts and digests for routine telemetry, bounded redacted examples for triage, and an access-controlled quarantine pointer for authorized repair. Protect schemas that reveal sensitive fields.

On failure, identify whether the defect is producer instance, schema definition, incompatible rollout, transform/cast, reference lag, rule bug, execution failure, or historical debt. Preserve input and result versions. Contain the affected publication or cohort rather than editing evidence.

Repair the earliest controlled cause. Backfill through transactional/idempotent paths, test repaired and unaffected controls, rerun the same suite, and publish a new version. Communicate changed schemas, excluded records, historical scope, and downstream replay requirements.

## Definitions and Notation

Let:

- $D_v$ be immutable dataset version $v$;
- $C_k=(S_k,R_k,P_k)$ be contract version $k$;
- $S_k$ be schema definition and dialect;
- $R_k$ be constraint rules and severities;
- $P_k$ be coverage, gating, and evidence policy;
- $Fields(S)$ map stable field identities to names/types/presence/defaults;
- $U_r(D_v)$ be rule $r$'s applicable population;
- $P_r(x)$ be its pass predicate;
- $s_r$, $f_r$, and $u_r$ be passed, failed, and unknown counts;
- $W_i$ and $R_j$ be writer and reader schema/client versions;
- $K(D)$ be the key multiset for dataset $D$; and
- $Ref_t$ be a pinned reference population at effective time $t$.

Schema conformance is a relation parameterized by dialect and options:

$$
SchemaOK(D_v,S_k,dialect,options).
$$

Rule result and coverage are

$$
Rate_r=\frac{s_r}{s_r+f_r},\qquad Coverage_r=\frac{s_r+f_r}{s_r+f_r+u_r}.
$$

When the intended universal population is empty, a universal predicate may be vacuously true; population completeness remains a separate requirement. When test execution cannot determine $P_r(x)$, count $x$ unknown rather than passing.

These definitions abstract over JSON Schema, Avro, Protocol Buffers, SQL databases, analytical formats, and test frameworks. Their exact nulls, defaults, compatibility, and enforcement semantics must come from the active specification and implementation version.

## Mechanisms, Invariants, or Proof Structure

Proof sketch for the limited meaning of a passing finite suite:

1. Let contract $C$ declare rule set $R=\{r_1,\ldots,r_n\}$ and complete evaluation populations.
2. Suppose every $r_i$ passes for all applicable members of pinned dataset $D$ and schema conformance passes.
3. By the definition of `Pass`, $D$ conforms to every declared critical predicate in $R$ under the suite's engine and policy.
4. Let property $q$ be a property not implied by the schema or any predicate in $R$, such as correspondence of a valid postal code to a person's real address.
5. Construct $D'$ identical with respect to every observation used by $R$ but with a false real-world address that remains syntactically valid.
6. The suite returns the same passing results on $D'$ while $q(D')$ is false.
7. Therefore passing the finite suite does not prove unspecified $q$; the result's valid claim is bounded conformance.

The argument assumes correct deterministic implementations and complete declared coverage for the positive conformance claim. Tool bugs, unsupported keywords, partial scans, stale references, and wrong contracts weaken even that claim.

The executable separates structural, row, uniqueness, and referential outcomes. It is a teaching abstraction, not a JSON Schema, Avro, Protobuf, SQL, distributed scan, or transactional enforcement engine.

<!-- bijux-verify: {"id":"layered-constraint-suite","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"schema_fields_ok=True\nrows=5\nrow_constraint_failures=('o3:amount_positive', 'o4:closed_requires_date')\nduplicate_keys=('o2',)\norphan_customer_keys=('c9',)\nsuite_pass=False\nrepaired_suite_pass=True\n","stderr":""}} -->
```python
expected_fields = {"order_id", "customer_id", "amount", "status", "closed_at"}
customers = {"c1", "c2", "c3", "c4"}
rows = [
    {"order_id": "o1", "customer_id": "c1", "amount": 10, "status": "open", "closed_at": None},
    {"order_id": "o2", "customer_id": "c2", "amount": 20, "status": "closed", "closed_at": "2026-09-01"},
    {"order_id": "o2", "customer_id": "c2", "amount": 5, "status": "open", "closed_at": None},
    {"order_id": "o3", "customer_id": "c9", "amount": -5, "status": "open", "closed_at": None},
    {"order_id": "o4", "customer_id": "c4", "amount": 8, "status": "closed", "closed_at": None},
]


def row_failures(records):
    failures = []
    for row in records:
        if row["amount"] <= 0:
            failures.append(f"{row['order_id']}:amount_positive")
        if row["status"] not in {"open", "closed"}:
            failures.append(f"{row['order_id']}:status_domain")
        if row["status"] == "closed" and row["closed_at"] is None:
            failures.append(f"{row['order_id']}:closed_requires_date")
    return tuple(sorted(failures))


def duplicate_keys(records):
    keys = [row["order_id"] for row in records]
    return tuple(sorted({key for key in keys if keys.count(key) > 1}))


def orphan_keys(records):
    return tuple(sorted({row["customer_id"] for row in records if row["customer_id"] not in customers}))


schema_ok = all(set(row) == expected_fields for row in rows)
failures = row_failures(rows)
duplicates = duplicate_keys(rows)
orphans = orphan_keys(rows)
print(f"schema_fields_ok={schema_ok}")
print(f"rows={len(rows)}")
print(f"row_constraint_failures={failures}")
print(f"duplicate_keys={duplicates}")
print(f"orphan_customer_keys={orphans}")
print(f"suite_pass={schema_ok and not failures and not duplicates and not orphans}")

repaired = [
    {"order_id": "o1", "customer_id": "c1", "amount": 10, "status": "open", "closed_at": None},
    {"order_id": "o2", "customer_id": "c2", "amount": 20, "status": "closed", "closed_at": "2026-09-01"},
    {"order_id": "o3", "customer_id": "c3", "amount": 5, "status": "open", "closed_at": None},
    {"order_id": "o4", "customer_id": "c4", "amount": 8, "status": "closed", "closed_at": "2026-09-02"},
]
repaired_ok = (
    all(set(row) == expected_fields for row in repaired)
    and not row_failures(repaired)
    and not duplicate_keys(repaired)
    and not orphan_keys(repaired)
)
print(f"repaired_suite_pass={repaired_ok}")
```

## Alternatives and Trade-Offs

**Closed versus open schemas.** Closed schemas catch typos and unexpected leakage. Open schemas support additive producers and forwarding unknown fields but require governance for unrecognized content.

**Registry compatibility versus fleet tests.** Registry algorithms are fast, consistent admission gates. Fleet round trips catch implementation, serialization-form, boundary-value, and semantic behavior the algorithm cannot know.

**Write-time enforcement versus asynchronous observation.** Enforcement prevents invalid committed state but supports limited predicates and adds write cost. Observation scales across rich relationships but creates a window requiring publication/quarantine design.

**Full versus incremental validation.** Full scans offer stronger coverage at cost. Incremental tests reduce latency but must include affected historical keys, parents, groups, windows, and rule changes.

**Exact versus probabilistic checks.** Exact scans support zero-tolerance claims. Sketches and sampling control cost and detect trends but need error bounds and cannot silently become proofs of absence.

**Schema defaults versus explicit migration.** Defaults preserve reader compatibility and rollout flexibility. They can hide missing producer behavior and blur source versus derived values unless presence is tracked.

**Strict parsing versus coercion.** Strict parsing exposes producer drift. Coercion accepts messy sources but can truncate, reinterpret timezones, turn malformed values null, or make incompatible types appear safe.

**Generic versus singular rules.** Reusable rule templates improve consistency and maintenance. Dataset-specific rules capture domain semantics; both need stable IDs, parameters, fixtures, and owners.

**Quarantine versus reject.** Quarantine retains good rows and evidence but changes population semantics. Reject preserves atomic completeness but can delay all data. Risk and consumer contract determine the gate.

**One central suite versus layered suites.** Central evaluation simplifies governance but detects defects late and can bottleneck. Layered producer/registry/staging/table/consumer checks shorten feedback while requiring deduplicated ownership and consistent evidence.

## Failure Modes and Misconceptions

1. **“It parsed, so it matches the schema.”** Parsing may validate only syntax/container structure.
2. **“Same fields means same schema.”** IDs, nesting, types, presence, defaults, and meaning matter.
3. **“Field order is identity.”** Stable IDs/numbers may define identity; positional systems need explicit order.
4. **“Default means optional.”** Serialization and reader-resolution semantics differ.
5. **“Decoded default was supplied.”** Reader materialization does not prove producer presence.
6. **“Null and absent are interchangeable.”** They can encode different information and compatibility behavior.
7. **“`format: email` always rejects invalid strings.”** JSON Schema dialect/vocabulary implementation determines assertion behavior.
8. **“Top-level closed means recursively closed.”** Nested scopes require their own applicable rules.
9. **“Backward compatible means safe.”** Direction, comparison window, values, and consumers must be named.
10. **“Wire compatible means lossless.”** Older/narrower readers can truncate or reinterpret values.
11. **“Removed Protobuf numbers can be reused.”** Reuse can corrupt interpretation; reserve them.
12. **“A schema registry validates every message.”** Compatibility admission and instance validation are separate.
13. **“`CHECK (x > 0)` rejects null.”** SQL unknown may satisfy check; add explicit not-null when needed.
14. **“Declared keys are enforced everywhere.”** Some analytical systems treat them as informational.
15. **“Unique means one row per person.”** Only if the key and temporal/entity grain say so.
16. **“One duplicate count is unambiguous.”** Groups, involved rows, and excess rows differ.
17. **“A foreign key can compare latest tables.”** Pin versions and effective-time semantics.
18. **“Late parents are orphans.”** A grace window may classify them pending.
19. **“Row checks cover dataset invariants.”** Keys, totals, and transitions need wider context.
20. **“Every valid snapshot has valid transitions.”** Illegal state changes can connect valid endpoints.
21. **“New enforcement validates history.”** Retrieve activation and backfill semantics.
22. **“Incremental means new rows only.”** Changed relationships can invalidate old rows.
23. **“A sample proves uniqueness.”** Rare duplicates can remain outside the sample.
24. **“Zero failures means pass.”** Coverage and execution status may be unknown.
25. **“A test cannot be wrong.”** Rule code, references, dialects, and thresholds need fixtures/review.
26. **“Waiving a rule removes the defect.”** It changes action temporarily, not observed facts.
27. **“Failure rows belong in logs.”** They can leak sensitive data.
28. **“Passing constraints proves accurate data.”** Conformance cannot establish untested reality.

## Worked Examples

### Example 1

A JSON document validates under Draft 2020-12 only when the declared vocabularies and implementation options are recorded. The team tests whether `format` is annotation or assertion and closes nested objects deliberately rather than assuming defaults.

### Example 2

An Avro reader adds `currency` with a default. Old data decodes, but completeness evidence records that old writers did not supply the field. Canary fixtures test aliases, union branches, decimals, and reader/writer directions.

### Example 3

A Protobuf field is retired. Its number and name are reserved, binary and JSON clients are tested separately, unknown enum values are exercised, and the rollout prevents new-range values until all narrow readers leave.

### Example 4

A database rule uses `amount NOT NULL` plus `CHECK (amount > 0)`. Fixtures test positive, zero, negative, and null because the check predicate alone would not reject SQL unknown.

### Example 5

An orders table declares a primary key in an analytical warehouse, but documentation says it is not enforced. A full observational uniqueness test gates publication; the declaration is labeled optimizer/documentation metadata, not protection.

### Example 6

A foreign-key check pins orders snapshot S9 and customers snapshot C7 at matching effective cutoff. Late customer records remain pending for two hours; after the grace window unresolved keys become failures.

### Example 7

An incremental uniqueness controller checks new keys against a maintained exact historical index, not merely against the new batch. It rebuilds/full-scans after index corruption or key-rule changes.

### Example 8

Both `open` and `closed` are valid statuses, but `closed → open` is forbidden except a named reopen event. Snapshot domain tests pass; the transition test catches an unrecorded reversal.

### Example 9

A validator loses access to one partition. It records execution unknown and 92% coverage, so the critical gate holds publication. Retrying does not overwrite the failed evidence record.

### Example 10

A rule upgrade runs advisory against six months of history, uncovers legitimate legacy exceptions, fixes a false-positive predicate, backfills actual defects, canaries clients, and only then becomes enforced. Exceptions remain versioned and time-bounded.

## Cross-Program Connections

- **Programming Languages:** type systems, algebraic data types, refinement types, parsing, serialization, and compiler diagnostics illuminate schemas and predicates.
- **Database Systems:** domains, checks, keys, referential actions, three-valued logic, transactions, deferred validation, indexes, and triggers shape enforcement.
- **Software Engineering:** contract tests, unit/property/mutation testing, fixtures, semantic versioning, compatibility matrices, CI, and code review govern suites.
- **API and Service Engineering:** OpenAPI/JSON Schema, protobuf, content negotiation, compatibility, idempotency, validation errors, and consumer-driven contracts parallel data interfaces.
- **Distributed Systems:** pinned snapshots, partial failure, eventual references, concurrency, retries, and consistency windows affect cross-dataset tests.
- **Platform Engineering:** registries, rule catalogs, test execution, policy gates, quarantine, evidence stores, and golden paths scale governance.
- **Security Engineering:** schema admission, malicious payloads, denial of service, sensitive fields, least privilege, evidence protection, and audit constrain validation.
- **Privacy Engineering:** minimization, purpose, defaults/imputation, protected failure rows, retention, correction, and erasure govern test artifacts.
- **Formal Methods:** predicates, quantifiers, invariants, transition systems, refinement, counterexamples, vacuous truth, and proof boundaries clarify guarantees.
- **Reliability Engineering:** coverage, unknown states, false passes/fails, SLOs, retries, incidents, blast radius, and recovery make testing operational.

## References

1. JSON Schema. [Draft 2020-12 specification](https://json-schema.org/draft/2020-12). Accessed 2026-09-03. Primary specification index for core, validation, vocabularies, unevaluated members, formats, output, and dialect behavior.
2. JSON Schema. [Validation vocabulary](https://json-schema.org/draft/2020-12/json-schema-validation). Accessed 2026-09-03. Primary specification for structural validation keywords, requiredness, numeric/string/object/array assertions, and format annotation/assertion.
3. Apache Avro. [Specification 1.12.0](https://avro.apache.org/docs/1.12.0/specification/). Accessed 2026-09-03. Primary specification for schemas, defaults, aliases, canonical forms, encoding, logical types, and writer-reader resolution.
4. Protocol Buffers. [Proto3 language guide](https://protobuf.dev/programming-guides/proto3/). Accessed 2026-09-03. Primary documentation for presence, defaults, unknown fields, enums, reserved identifiers, binary compatibility, and conditional compatibility.
5. Confluent. [Schema evolution and compatibility](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html). Accessed 2026-09-03. Primary registry documentation for backward, forward, full, transitive, and subject-level compatibility modes.
6. PostgreSQL. [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html). Accessed 2026-09-03. Primary database documentation for check/null truth, not-null, unique, primary, foreign-key, exclusion, cross-row limitations, and enforcement.
7. Apache Iceberg. [Schemas](https://iceberg.apache.org/docs/latest/schemas/). Accessed 2026-09-03. Primary table-format documentation for field identities, supported/logical types, nullability, and safe evolution.
8. Delta Lake. [Constraints](https://docs.delta.io/delta-constraints/). Accessed 2026-09-03. Primary table-format documentation for enforced not-null/check constraints, existing-row validation, failures, and protocol implications.
9. dbt Labs. [Data tests](https://docs.getdbt.com/docs/build/data-tests). Accessed 2026-09-03. Primary documentation for generic/singular SQL assertions, failure rows, and standard uniqueness, non-null, accepted-value, and relationship tests.
10. Great Expectations. [Validate data schema](https://docs.greatexpectations.io/docs/reference/learn/data_quality_use_cases/schema/). Accessed 2026-09-03. Primary documentation for column/table schema expectations, types, order, required fields, and validation history.
11. Great Expectations. [Validate data integrity](https://docs.greatexpectations.io/docs/reference/learn/data_quality_use_cases/integrity/). Accessed 2026-09-03. Primary documentation for referential, cross-column, cross-table, and custom business-rule validation.
12. W3C. [Shapes Constraint Language](https://www.w3.org/TR/shacl/). Accessed 2026-09-03. W3C Recommendation for graph shapes, constraints, severities, conformance reports, validation results, and execution failures.
13. Schelter et al. [Automating large-scale data quality verification](https://www.vldb.org/pvldb/vol11/p1781-schelter.pdf). Accessed 2026-09-03. Peer-reviewed primary paper for analyzers, constraints, verification, metric repositories, suggestions, anomaly detection, and incremental computation.
14. OpenAPI Initiative. [OpenAPI Specification 3.1.1](https://spec.openapis.org/oas/v3.1.1.html). Accessed 2026-09-03. Primary API specification integrating a JSON Schema dialect and defining schema objects, validation, examples, and compatibility-relevant interface structure.

## Exercises

### Exercise 1

Design a versioned contract for an order event carried as Protobuf into Avro storage and an Iceberg table. Include field identities, presence/null/defaults, logical types, unknown fields, key/grain, domains, transitions, canonical digests, and cross-format mappings.

### Exercise 2

Create a producer-consumer compatibility test matrix for three historical and one proposed schema version. Cover backward/forward/transitive directions, binary versus JSON, aliases, removed/reserved fields, enums, numeric boundaries, unknown preservation, semantic equivalence, dormant clients, and activation gates.

### Exercise 3

Specify a constraint suite for customers, orders, order lines, and daily ledger balances. Include not-null/domain/range, composite uniqueness, temporal foreign keys, cardinality, header-line aggregates, balance reconciliation, status transitions, null semantics, tolerances, and references.

### Exercise 4

Design a scalable full-plus-incremental validation architecture. Cover pinned versions, affected historical scope, exact indexes/sketch limitations, partitions, coverage, execution unknowns, privacy-aware evidence, publication gating, retries, and periodic full rebuilds.

### Exercise 5

Plan rollout of a new critical rule on a five-year table with violations and six clients. Include advisory history scan, rule fixtures/mutation tests, remediation, exceptions, producer and reader canaries, enforcement matrix, waiver expiry, monitoring, and rollback/forward correction.

## Answers to the Exercises

### Answer 1

Assign immutable event `order_id` and event sequence as grain/key; reserve Protobuf numbers/names on removal and map them to immutable Avro/table field identities. Record each schema's dialect/version/digest and mappings for nested fields, enums, decimal amount/currency, event instant/timezone, repetition, optional presence, explicit null unions, and reader defaults. Preserve unknown binary fields where forwarding requires it and test JSON separately. Constraints require positive amount, known currency/status, customer identity, unique `(order_id,sequence)`, monotonic sequence, and allowed status transitions. Defaults remain reader-derived, not proof of source presence. Mappings and logical-type conversions have round-trip boundary fixtures and named loss policy. Registry, storage, and table schemas advance through one reviewed compatibility release.

### Answer 2

Enumerate every writer $W_1..W_4$ against required readers $R_1..R_4$ in both directions required by rollout, plus transitive endpoint comparisons. For each pair, encode and decode binary fixtures and separately JSON/text fixtures containing absent/present defaults, removed and reserved fields, old/new enum values, nested/oneof/union branches, Unicode, decimal/timestamp extremes, and widened values beyond old ranges. Assert semantic values, presence, unknown preservation, and reserialization—not parse alone. Exercise Avro aliases/default resolution and Protobuf tag/name rules. Include dormant exporter and recovery binaries. The proposed version remains advisory until all required cells pass or clients are formally retired; then deploy readers, producers constrained to old value ranges if needed, activate new values, and monitor incompatible attempts.

### Answer 3

Define table UUID/snapshots, entity/event grain, and suite version. Customers require stable non-null customer key and effective intervals without overlap. Orders require unique order ID, valid status/currency, positive amount, and customer resolution at order effective time with explicit late-parent/null/deletion rules. Lines require unique `(order_id,line_no)`, positive quantity/nonnegative price, and order reference. Header amount equals rounded line sums under one currency/rounding rule; daily ledger opening plus transactions equals closing within declared tolerance from independently derived sides. Status changes follow an allowed graph with event sequence. SQL checks pair not-null with predicates so unknown cannot pass accidentally. Report counts for duplicate groups/rows/excess, orphans/pending, aggregate mismatches, transition failures, coverage/unknowns, pinned references, and severity.

### Answer 4

Pin data, parent/reference, schema, and rule versions per run. Full scans evaluate every applicable row/key/relation initially, after rule/index changes, and periodically. Incremental runs validate new/changed rows plus historical keys that can duplicate, children affected by parent changes, groups/windows touched by late events, and transition predecessors. Maintain exact key/reference states transactionally with provenance; sketches may prioritize or filter only when their error cannot hide a violation. Record intended versus scanned partitions/rows/bytes, query plans, exclusions, errors, and reference freshness. Permission/timeouts become unknown and hold critical publication. Store counts/digests and bounded redacted samples with a controlled quarantine pointer. Retries are idempotent and append evidence. Rebuild states after detected drift/corruption and compare incremental with full results on canaries.

### Answer 5

Version the proposed rule with owner, rationale, exact population/null semantics, severity, and historical/future scope. Unit fixtures include pass/fail/null/boundary/malformed cases; mutation/injected defects must make it fail. Run advisory over all five years and recent increments, classify true defects versus rule errors, correct the predicate, remediate/backfill transactionally, and record legitimate exceptions by cohort/effective period. Test every reader/writer/maintenance/recovery client and enumerate which paths enforce versus observe. Canary readers and producers, then activate the publication gate or transactional constraint only after historical critical failures are zero or explicitly approved. Waivers retain observed failure, risk, compensating control, owner, and automatic expiry. Monitor coverage, unknowns, violations, incompatible writes, false-positive disputes, waiver age, and escaped incidents. Roll back disposition/routing if the rule is faulty; correct data forward without deleting evidence.
