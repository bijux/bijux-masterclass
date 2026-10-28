---
module_id: DE-008
program: Data Engineering
level: 1
module_number: 8
title: Schemas, Nullability, and Type Fidelity
status: complete
last_verified: 2026-09-02
---

# Schemas, Nullability, and Type Fidelity

## One-Page Review

### Governing question

How should a data engineer specify, translate, validate and evolve schemas so that values retain their domain meaning and presence state across files, messages, databases, languages and analytical systems?

### Essential definitions

- A **schema** names fields and constrains their structural shapes, types, presence and relationships at a boundary.
- A **physical type** describes representation, such as signed 64-bit integer or byte array. A **logical type** interprets that representation, such as decimal or timestamp. A **domain type** adds business meaning, such as account identifier or ISO currency amount.
- **Null** is an explicit no-value marker supported by a representation. **Missing** means the field or observation was absent. They are not inherently equivalent.
- A **default** is a rule for resolving an omitted value in a particular operation. It does not prove that a producer observed or transmitted that value.
- **Type fidelity** is preservation of governed value distinctions, range, precision, scale, units, presence and meaning through a transformation.
- **Round-trip fidelity** holds when decoding an encoded domain state yields an equivalent state under an explicit domain equivalence relation.
- A **constraint** narrows allowed instances, for example with a range, pattern, enum, uniqueness rule or cross-field invariant.
- **Schema evolution** changes a schema while controlling which old and new readers can process old and new data.
- A **field identifier** is a stable identity independent of a mutable display name; systems that resolve fields by ID can distinguish rename from drop-and-add.
- **Coercion** converts a value to another type. It is safe only when its acceptance policy and information-loss behavior are explicit.

### Central model, mechanism, or theorem

Describe a field as

$$
F=(id,name,P,L,D,S,C,U,V),
$$

where $P$ is physical type, $L$ logical type, $D$ domain meaning, $S$ presence-state policy, $C$ constraints, $U$ unit and $V$ contract version. For source state $x$, encoder $e$ and decoder $d$, fidelity requires

$$
d(e(x))\equiv_D x.
$$

The equivalence must cover values and meaningful states, not merely similar printed output. If two distinct source states map to one target state, the mapping is non-injective and no decoder can reconstruct the distinction without side information. Therefore a default-valued read cannot prove producer observation when both missing and explicitly default-valued inputs resolve to the same value.

### Critical invariants

- Missing, explicit null, empty, zero, false, invalid, unknown, not applicable and redacted remain distinct whenever the domain distinguishes them.
- Every field has a declared physical type, logical interpretation, domain meaning, range, unit and presence policy.
- Decimal precision and scale, integer range and signedness, floating exceptional values, text normalization and temporal semantics are explicit.
- Container nullability and element nullability are modeled separately at every nesting level.
- Conversions reject or quarantine values that cannot be represented faithfully; they do not silently narrow, round, wrap, truncate or invent provenance.
- Defaults are applied only at named read/write/business operations and never rewritten as historical facts without provenance.
- Evolution preserves field identity, reserves retired identifiers, inventories reader/writer compatibility and has a rollback path.
- Round-trip, boundary and adversarial fixtures traverse every real serialization hop, not only an in-memory library call.
- Validation records rejected counts and reasons while preserving raw evidence for authorized repair.
- Security and privacy states such as redacted are not encoded as ordinary null unless that collapse is explicitly acceptable.

### Common failures

Treating a schema as field names plus primitive types; inferring a durable schema from a convenient sample; assuming optional means nullable; collapsing missing, null and default; encoding identifiers as floating-point numbers; using binary float for exact money; dropping decimal scale or currency; accepting integer overflow or signedness changes; converting bytes to text without an encoding; comparing Unicode by raw bytes without a normalization contract; treating empty strings as universal nulls; confusing a nullable list with nullable elements; mapping unknown enum values to a valid member; reusing a retired field number; renaming a name-resolved column as if it had stable identity; adding a required field without a compatibility plan; and calling successful parsing proof of semantic fidelity.

### Compact example

A discount field has four inputs: missing, explicit null, integer zero and empty string. A governed classifier retains `missing`, `null`, `present:0` and `invalid:str`. A read default may resolve both missing and explicit zero to `0`, but the equal reads do not make their source states equal. The empty string is quarantined rather than coerced. The same boundary verifies that an `int32` maximum widens to `int64` and returns exactly, while `2^31` is rejected by an `int32` target.

### Connections

[DE-003](003-csv-json-and-line-oriented-formats.md) introduces schema-poor interchange; [DE-004](004-avro-protocol-buffers-and-schema-aware-serialization.md) compares schema-aware formats; [DE-005](005-arrow-and-in-memory-columnar-representation.md) and [DE-006](006-parquet-and-columnar-files.md) expose physical/logical types and validity structures. Time semantics continue in the next module. Contracts connect to [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), domain meaning to [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), and privacy states to [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

Which distinctions must survive every data boundary, and how can a schema make those distinctions testable rather than implicit?

A schema is an executable agreement between producers, storage systems, processing engines and consumers. It says more than “this field is an integer.” Is the integer signed? What range is legal? Is it an identifier, a count or a scaled amount? Is absence allowed? Does zero mean measured zero, unknown, not applicable or an application default? Can a reader distinguish those cases after serialization?

Type fidelity is boundary-relative. A value may fit in the source language yet exceed the target format; fit physically yet lose its logical annotation; retain its printed digits yet lose decimal scale; preserve code points yet compare differently because normalization or collation changed. A pipeline is faithful only under a declared equivalence that reflects the domain.

Primary specifications expose the differences. [JSON](https://www.rfc-editor.org/rfc/rfc8259.html) has a compact type vocabulary and warns that numeric interoperability depends on implementation limits. [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-validation.html) separates the `required` property constraint from value types, so a property can be required and still accept null only if its schema admits null. [Avro 1.12](https://avro.apache.org/docs/1.12.0/specification/) distinguishes primitive and logical types and defines defaults as reader-side resolution for absent fields. [Protocol Buffers field presence](https://protobuf.dev/programming-guides/field_presence/) shows why implicit default-valued APIs cannot always tell “never set” from “set to the default.”

The engineering task is to turn domain distinctions into representation, validation, compatibility and telemetry rules. A parser accepting bytes is the beginning of that task, not the end.

## Why This Matters

Schema errors often look plausible. A 64-bit identifier rounded by a floating intermediary is still a number. A money amount converted from decimal to binary float still prints near the expected value. A missing laboratory result defaulted to zero still participates in an average. A renamed column resolved by name may appear as a deleted old field and unrelated new field. These failures can survive syntactic validation and contaminate downstream decisions.

Nullability changes behavior. SQL filters, joins, aggregates and constraints commonly treat null through three-valued logic or null-specific rules. Dataframes and languages may use separate sentinels, option types, masked arrays or special floating values. A conversion that collapses these representations can change row counts, group membership, alerts and model features.

Schema inference is attractive at ingestion because it reduces setup. Yet a finite sample cannot establish a universal type. Early account identifiers may contain digits only; later ones may have leading zeros or letters. A column observed with small integers may later exceed 32 bits. A sample without nulls cannot prove non-nullability. Inference should propose a provisional schema and attach evidence, never silently establish a durable contract.

Evolution creates distributed risk. Readers and writers deploy at different times, retained files outlive services, replay revisits old bytes, and recovery tooling is often older than the primary path. Compatibility must therefore be evaluated as a matrix: old reader/new data, new reader/old data, old writer/new schema, and new writer/old consumers. “The registry accepted it” is evidence for one configured rule set, not proof for every consumer.

Privacy gives absence another dimension. A redacted value may have existed and been withheld; a missing value may never have been collected; not applicable means the question did not apply. Collapsing all three to null can undermine auditability, consent enforcement and safe analysis.

## Prerequisites and Retrieval

Retrieve the authoritative domain definitions; producing and consuming teams; sample payloads including rejected records; every schema version; registry compatibility rules; file and wire format specifications; database DDL; language bindings; generated code versions; physical storage schemas; logical annotations; integer widths and signedness; decimal precision and scale; units and currencies; string encodings; Unicode normalization and collation settings; enum definitions and unknown-value behavior; timestamp kinds and precision; field identifiers and reserved identifiers; required, optional and nullable rules; defaults and the operations that apply them; nested container and element nullability; constraint definitions; coercion settings; inference sample size and ordering; rejected-value handling; raw retention; validation telemetry; historical files; replay and rollback tooling; privacy classifications; redaction reasons; and all serialization hops from source to final consumer.

Distinguish missing from null; null from empty; empty from zero; default from observed; invalid from unknown; unknown from unrecognized enum; not applicable from not collected; redacted from absent; optional property from nullable value; nullable collection from collection containing null elements; primitive type from logical type; logical annotation from domain meaning; bytes from encoded text; Unicode scalar sequence from grapheme presentation; normalization from locale collation; precision from scale; integer widening from semantic widening; representation compatibility from domain compatibility; reader compatibility from writer compatibility; name from stable field identity; parsing from validation; validation from repair; and exact round trip from merely similar display.

Establish a retrieval record: source URL or repository path, version, retrieval date, owner and applicability. Generated client classes are useful evidence of a toolchain, but the governed schema and normative format specification remain the contract. Preserve representative boundary fixtures alongside schema versions so the next evolution can replay the same distinctions.

## Learning Objectives

After completing this module, you should be able to:

1. model physical, logical and domain types as separate but connected layers;
2. distinguish missing, null, empty, default, unknown, invalid, not applicable and redacted states;
3. specify integer, decimal, floating, text, binary, enum, temporal and nested-type fidelity;
4. evaluate conversions for range, precision, scale, units, normalization and provenance loss;
5. design explicit ingestion validation, coercion and quarantine policies;
6. prove when a collapsed mapping cannot be inverted;
7. construct cross-format round-trip and compatibility matrices;
8. evolve schemas using stable field identities and safe retirement rules;
9. monitor null/type drift and rejected values without concealing data loss; and
10. document schema decisions so producers and consumers can test the same contract.

## Core Exposition

### Treat a schema as a layered contract

Begin with five layers. Syntax describes which tokens or wire constructs are legal. Physical type describes how bits are stored. Logical type interprets the physical representation. Domain type supplies business meaning. Presence and quality state say whether a meaningful value exists and why it may not.

The layers can change independently. Parquet may physically store a string as `BYTE_ARRAY` with a logical string annotation. A decimal can be an unscaled integer plus precision and scale. An account ID may be physically UTF-8 text yet forbid trimming, case folding or numeric interpretation. Losing an annotation can leave readable bytes with wrong semantics.

Write all layers into the contract or linked metadata. Names help humans but do not replace definitions. “amount” without currency, unit, rounding rule and decimal bounds is incomplete.

### Model presence before choosing a nullable type

Use an explicit state vocabulary appropriate to the domain. A useful general model is:

$$
State_F=Missing\mid Null\mid Present(v)\mid Invalid(e)\mid Redacted(r).
$$

Applications may add `NotApplicable`, `NotCollected`, `Pending` or `Unknown`, but each addition needs behavior at storage, query, export and display boundaries.

Missing is structural absence. Null is an explicit value marker. Empty string and empty collection are present values. Zero and false are present values. Invalid means evidence arrived but violated the contract. Redacted means a value or possibility was deliberately withheld. These are not interchangeable unless the domain declares them equivalent.

Do not encode every state as a magic scalar such as `-1`, `9999-12-31` or `UNKNOWN`. Magic values pollute numeric operations and can collide with future valid values. Prefer a tagged state, companion reason field or governed union.

### Separate optional from nullable

An optional field may be absent. A nullable field may be present with null. A field can be required and nullable, optional and non-null when present, both optional and nullable, or neither.

JSON Schema demonstrates this orthogonality: object `required` lists property names that must occur, while the property's `type` determines whether `null` is accepted. API descriptions and language generators sometimes use “optional” ambiguously, so test generated behavior with absent and explicit-null fixtures.

In patch semantics the distinction is especially important. Missing may mean “leave unchanged,” null may mean “clear,” and a present value may mean “set.” A representation that collapses missing and default cannot express every patch.

### Define defaults as operations

A default is not a fact about the source. Name where it applies: schema reader resolution, database insertion, UI presentation, query expression or domain command. Avro specifies a record-field default for reading instances that lack the field; it does not make the field optional at encoding time and values equal to defaults are still encoded.

Track whether a value was observed, supplied, inferred or defaulted when that provenance matters. Materializing a default into historical data may be a legitimate migration, but it changes knowledge state and needs an explicit policy.

Never infer “the producer sent zero” from an API that returns zero for an absent field. Protocol Buffers documents the difference between implicit and explicit presence. Use explicit presence where the domain needs it.

### Specify integer fidelity

Declare signedness, bit width and allowed domain range. A physical `int64` can hold more than a domain counter is allowed to use; both constraints matter.

Widening a signed 32-bit integer to signed 64-bit preserves every source value. The reverse is a partial conversion and must check `-2^31 <= x < 2^31`. Unsigned-to-signed conversion needs a range check even at equal width. Never rely on wraparound, saturation or implementation-defined casts at a data boundary.

JSON syntax does not declare an integer width. RFC 8259 notes broad exact interoperability for integers within `[-(2^53)+1,(2^53)-1]` when implementations use binary64-like limits. Send larger identifiers as strings or use a negotiated representation when any consumer may traverse that number model.

Identifiers are not quantities. Even if an identifier contains only digits, arithmetic, exponent notation, sign normalization and removal of leading zeros are usually invalid. Model identifiers as constrained strings or dedicated domain types.

### Preserve exact decimals

Exact quantities such as currency commonly need decimal arithmetic. Model a decimal as an unscaled integer $u$ and scale $s$:

$$
x=u\times10^{-s}.
$$

Precision bounds the total decimal digits; scale bounds fractional digits. `12.30` and `12.3` may be numerically equal but scale can matter for presentation, measurement resolution or contractual pricing.

Parquet's decimal logical type records precision and scale over an allowed physical representation. Avro similarly defines decimal as a logical type over bytes or fixed storage. Preserve the annotation and validate that scale does not exceed precision. When rescaling, declare whether exact divisibility is required or which rounding rule applies.

Do not route exact decimals through binary floating point. Parse, calculate and serialize with decimal-aware types or unscaled integers. Include maximum magnitude, negative values, zero at each relevant scale and halfway rounding cases in tests.

### Govern floating-point exceptional values

Binary floating point is appropriate for many measurements and numerical workloads, but it is not exact decimal arithmetic. Declare width, rounding expectations and policy for NaN, positive/negative infinity and signed zero.

Exceptional values interact with equality, ordering, hashing, aggregation and serialization. JSON does not provide number tokens for NaN or infinities. A serializer might reject them, stringify them or emit non-standard tokens. Choose one explicit boundary behavior and test it.

Avoid using NaN as a universal missing marker when another layer supports null. A floating NaN is a present floating value with exceptional numerical behavior; null is a presence state. Converting between them loses a distinction unless the schema says they are equivalent.

### Distinguish text from bytes

Bytes are uninterpreted octets until an encoding or protocol assigns meaning. Text requires an encoding such as UTF-8. Never decode arbitrary bytes by guessing or by silently replacing invalid sequences when exact fidelity matters.

Unicode permits canonically equivalent text to have different code-point sequences. [Unicode Standard Annex #15](https://www.unicode.org/reports/tr15/) defines normalization forms such as NFC and NFD. Choose a normalization policy for comparison keys and enforce it consistently. Normalization does not define locale-sensitive collation, case folding, grapheme segmentation or identifier security; those need separate policies.

Preserve original display text when normalization is used to derive a matching key. Compatibility normalization can erase distinctions that matter in some domains. Test composed/decomposed accents, non-ASCII scripts, combining marks, emoji sequences, embedded NUL, invalid UTF-8 and normalization at concatenation boundaries.

### Model enums for evolution

An enum gives a closed symbolic vocabulary at a schema version. Decide what a newer producer's unknown member does at an older consumer: preserve its numeric/tag identity, surface an unknown wrapper, route to quarantine or fail. Mapping it to an existing valid member invents meaning.

Reserve a neutral zero member when a format requires one, but do not confuse that member with missing. Retire names and numeric identifiers without reuse. If the domain is intentionally open-ended, a validated string vocabulary with unknown preservation may be safer than a closed generated enum.

### Model nested nullability at every level

For `list<T>`, ask separately whether the list can be null and whether each element can be null. The states null list, empty list, list containing null and missing field are four different structures.

The same rule applies to maps, records and unions. A nullable parent struct can hide child buffers physically, but child nullability remains separately defined. Apache Arrow's [columnar format](https://arrow.apache.org/docs/format/Columnar.html) gives nested arrays their own validity bitmap, illustrating that parent and child validity are distinct.

Write fixtures for every nesting boundary. Many generated bindings cannot express all theoretical combinations, and some query engines flatten or reconstruct them differently.

### Make constraints executable

Primitive types allow more values than most domains. Add range, length, pattern, enum, precision, uniqueness, referential and cross-field constraints where enforcement is possible.

Separate structural validation from domain validation. A birth date can be syntactically valid yet impossible relative to another field; an amount can fit decimal storage yet use the wrong currency scale. Record which layer owns each rule and when it runs.

Constraints involving external state, such as uniqueness or referential existence, cannot be established by a record schema alone. Describe transaction scope, lateness and reconciliation instead of pretending a local parser proves them.

### Use inference as evidence, not authority

An inferred schema depends on sample selection, ordering, parser heuristics, locale and thresholds. Preserve those parameters and the sample digest. Infer into the widest safe provisional type, compare against the governed contract and require review for promotions.

Leading-zero strings, empty fields, scientific notation, large integers and mixed date forms are adversarial inference cases. Sample the tail and rare partitions, not only the first block. Monitor later values against the approved schema.

When no contract exists, land raw immutable data first, infer a candidate, profile it, obtain domain ownership and publish a versioned schema. Do not rewrite raw evidence to match the candidate silently.

### Define coercion as a decision table

For each source/target pair, specify accepted lexical forms, whitespace, signs, bases, locale, overflow, rounding, loss and failure action. “Cast to integer” is not a policy.

Classify conversions as exact total, exact partial, lossy accepted with rule, or forbidden. Integer widening can be exact total for the source domain. String-to-integer is partial. Decimal-to-binary-float is generally lossy. Bytes-to-text is partial under a declared encoding.

Keep invalid input and error reason in quarantine. A repair job may later transform it with authorization, lineage and idempotence. Coercion counts should be observable because a rising success-by-coercion rate often signals producer drift.

### Preserve field identity through evolution

Names change; identity should not. Formats with numeric or stable field IDs can resolve a rename without interpreting it as a deletion plus addition. [Apache Iceberg's specification](https://iceberg.apache.org/spec/) uses field IDs for schema evolution and requires uniqueness, illustrating the durability benefit.

Never reuse a retired field ID or number for different meaning. Old bytes would be decoded as the new field. Reserve retired identifiers and names according to the format. Do not change a field's domain meaning merely because its physical representation remains compatible.

For name-resolved systems, use explicit aliases or migrations where supported and test old files. Case sensitivity and normalization of field names are themselves contract choices.

### Evaluate compatibility in both directions

Backward compatibility commonly asks whether a new reader can read old data. Forward compatibility asks whether an old reader can tolerate new data. Full compatibility requires both under stated rules.

Adding an optional field may be structurally safe if old readers ignore unknowns and new readers handle absence. It may still be operationally unsafe if a new producer relies on the field for authorization or money calculation. Adding a required field can fail old data unless reader resolution supplies a justified default or a migration populates evidence.

Build a matrix of deployed readers, writers, stored versions and recovery tools. Test binaries, not only abstract schemas. Consumer-first deployment is useful when new readers must understand both old and new representations before writers emit the new one.

### Test semantic round trips

For transformation $T$ and inverse candidate $R$, test $R(T(x))\equiv_D x$ over boundary and adversarial states. Byte equality may be stronger than necessary for normalized formats; display equality is usually too weak. Define equivalence explicitly.

Traverse the real path: source binding to JSON gateway to event schema to columnar memory to file to query engine to export. Pairwise library tests can miss loss introduced by the composition.

Maintain a mapping matrix with source type, target type, allowed range, presence mapping, precision/scale behavior, unknown handling and proof fixture. Any many-to-one mapping must identify the intentionally lost distinction or add side information.

### Observe fidelity in production

Measure records accepted, rejected and coerced; missing/null/empty rates by field; min/max and precision; enum unknowns; invalid UTF-8; normalization changes; decimal rescaling; overflow rejections; schema-version distribution; default application; and consumer decode errors.

Alert on rates and distribution shifts, not merely schema registration. A producer can remain type-valid while changing units or populating every value with a default. Compare to domain expectations and release events.

Telemetry must respect privacy. Report aggregates and reasons without leaking sensitive raw values. Preserve authorized raw evidence with retention and access controls for repair.

## Definitions and Notation

Let a governed field be

$$
F=(id,name,P,L,D,S,C,U,V).
$$

Here `id` is stable identity; `name` is a human-facing label; $P$ is physical type; $L$ is logical interpretation; $D$ is domain meaning; $S$ is the allowed state set; $C$ is constraints; $U$ is unit/currency; and $V$ is contract version.

Let $X_F$ be the source-state domain and $Y_G$ the target-state domain. A conversion $c:X_F\rightharpoonup Y_G$ may be partial. It is exact on governed set $A\subseteq X_F$ when every $x\in A$ is accepted and an inverse $r$ satisfies

$$
r(c(x))\equiv_D x.
$$

The equivalence relation $\equiv_D$ states which distinctions the domain permits a representation to ignore. Numeric equality might permit decimal `12.3` and `12.30` to compare equal, while a measurement-resolution domain might not.

For integer target range $[m,M]$, a cast accepts only $m\leq x\leq M$. For decimal precision $p$ and scale $s$, values use unscaled integer $u$ with $x=u10^{-s}$ and typically require $0\leq s\leq p$ plus the format's magnitude bound.

Define state counts $n_s$ and rate $q_s=n_s/N$ for each governed presence/quality state $s$. A drift comparison can use $\Delta q_s=q_{s,t}-q_{s,baseline}$, interpreted with volume, seasonality and release context.

A compatibility matrix $K(r,w,d)$ records whether reader version $r$ correctly interprets data written by writer $w$ under domain fixtures $d$. Syntactic decode alone does not make $K$ true.

## Mechanisms, Invariants, or Proof Structure

Use this mechanism for a new or changed data boundary:

1. Name the producer, consumer, grain, domain owner and retention horizon.
2. Inventory every existing physical, logical, domain and presence representation.
3. Enumerate meaningful states, including invalid and privacy-related absence reasons.
4. Declare field identity, names, types, units, constraints, defaults and version.
5. Construct a source-to-target mapping table for every hop.
6. Classify each conversion as exact total, exact partial, governed lossy or forbidden.
7. Define rejection, quarantine, retry and repair behavior before accepting input.
8. Create minimum, maximum, empty, null, missing, unknown and malformed fixtures.
9. Add format-specific cases for decimals, floats, Unicode, enums, nesting and time.
10. Execute end-to-end round trips through production libraries and configurations.
11. Build the old/new reader-writer compatibility matrix, including recovery tools.
12. Deploy tolerant readers and observability before producers emit a new form.
13. Canary writers, inspect fidelity telemetry and retain a reversible path.
14. Reserve retired field identities and retain old schemas as long as data survives.
15. Audit defaults, coercions and repairs as lineage-bearing transformations.
16. Revalidate after library, engine, schema-registry or configuration upgrades.

The executable model keeps source presence separate from a resolved read value and checks a widening/narrowing boundary. It is deliberately a small semantic fixture, not evidence about a particular serialization library.

<!-- bijux-verify: {"id":"type-fidelity-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"states=('missing', 'null', 'present:0', 'invalid:str')\naccepted=3 quarantined=1\nresolved_default_pair=(0, 0)\nsource_states_distinct=True\nwidening_round_trip=True\nnarrowing_rejected=True\n","stderr":""}} -->
```python
def classify(record, field):
    if field not in record:
        return ("missing", None)
    value = record[field]
    if value is None:
        return ("null", None)
    if type(value) is int and 0 <= value <= 100:
        return ("present", value)
    if type(value) is str:
        return ("invalid", "str")
    return ("invalid", "other")


def label(state):
    if state[0] == "present":
        return "present:" + str(state[1])
    if state[0] == "invalid":
        return "invalid:" + state[1]
    return state[0]


records = ({}, {"discount": None}, {"discount": 0}, {"discount": ""})
classified = tuple(classify(record, "discount") for record in records)
states = tuple(label(state) for state in classified)
accepted = sum(1 for state in classified if state[0] != "invalid")
quarantined = len(classified) - accepted

missing_read = 0 if classified[0][0] == "missing" else classified[0][1]
explicit_zero_read = classified[2][1]
resolved_default_pair = (missing_read, explicit_zero_read)

int32_min = -(2 ** 31)
int32_max = 2 ** 31 - 1
source = (int32_min, -1, 0, 1, int32_max)
widened = tuple(int(value) for value in source)
round_trip = tuple(value for value in widened if int32_min <= value <= int32_max)
candidate = 2 ** 31

print("states=" + str(states))
print("accepted=" + str(accepted) + " quarantined=" + str(quarantined))
print("resolved_default_pair=" + str(resolved_default_pair))
print("source_states_distinct=" + str(classified[0] != classified[2]))
print("widening_round_trip=" + str(round_trip == source))
print("narrowing_rejected=" + str(not (int32_min <= candidate <= int32_max)))
```

Critical invariants are:

- **Identity:** stable field IDs are unique and retired IDs are never reassigned.
- **State:** every meaningful input state maps explicitly or is rejected with evidence.
- **Range:** accepted numeric values fit both physical representation and domain bounds.
- **Exactness:** precision, scale, sign, exceptional values and units follow declared rules.
- **Text:** byte encoding, normalization and comparison policies are versioned and tested.
- **Nesting:** validity of each container and child level is independently preserved.
- **Evolution:** every deployed reader/writer/data combination has a known result.
- **Provenance:** defaults, inference, coercion, redaction and repair never masquerade as observation.

**Proof sketch — a resolved default cannot prove producer observation.** Let source states $a=Missing$ and $b=Present(0)$ be distinct. Suppose reader resolution $g$ supplies default zero for missing and returns present integers unchanged. Then $g(a)=0=g(b)$. Thus $g$ is not injective. If an inverse $h$ reconstructed the source state from the resolved value, it would need both $h(0)=a$ and $h(0)=b$, impossible because $a\neq b$. Recovering the distinction requires side information such as explicit presence or provenance. This does not prohibit defaults; it limits what can be inferred after applying them.

## Alternatives and Trade-Offs

**Strict rejection versus coercion.** Strict boundaries expose drift early and preserve contract clarity, but can interrupt availability. Governed coercion can absorb harmless lexical differences, but it adds ambiguity and can normalize producer defects. Use a decision table, limits, telemetry and raw quarantine rather than a global permissive parser.

**Closed versus open schemas.** Closed objects reject unknown fields and catch misspellings, but make additive evolution harder. Open objects tolerate new producers, but may hide ignored critical fields. A common compromise is open transport for forward compatibility plus explicit capture/telemetry of unknown fields and closed domain commands where safety requires it.

**Required versus optional fields.** Required fields simplify consumers and expose incomplete records. Optional fields support gradual rollout and genuinely unavailable observations. Do not mark everything optional merely to avoid ingestion failures; model ownership and completeness targets.

**Null versus tagged absence.** A single null is compact and widely supported. Tagged unions or reason companions retain why a value is absent but increase schema and query complexity. Use tags when decisions, privacy or audit depend on the reason.

**Numeric identifier versus string identifier.** Integers can be compact and sortable, but invite arithmetic, lose leading zeros and may exceed intermediary precision. Strings preserve lexical identity across JSON and languages at some storage/index cost. Dedicated binary identifiers can be efficient but require exact conversion tooling.

**Binary float versus decimal.** Floating point offers broad hardware acceleration and scientific range. Decimal preserves base-10 quantities and rounding rules. Choose by domain operations, not familiarity. Some systems should carry both a raw measurement float and a separately rounded reporting decimal.

**Schema-on-write versus schema-on-read.** Write-time enforcement stops invalid data early and makes shared assets predictable. Read-time interpretation supports raw exploration and changing views. Durable systems often retain immutable raw evidence while publishing schema-on-write curated products.

**Name-based versus ID-based evolution.** Name resolution is readable and common but makes renames ambiguous. Stable IDs support safe rename and nested evolution but require governance, non-reuse and compatible tooling. If the format is name-based, aliases and explicit migration plans approximate identity at greater operational cost.

**Defaulted evolution versus backfill.** Reader defaults make old data readable without rewriting it, but the value is derived and may vary with reader schema. Backfill materializes a governed value and simplifies later reads, but costs compute, changes lineage and may incorrectly claim historical knowledge. Preserve provenance either way.

**Central registry versus repository-owned schemas.** A registry can enforce compatibility and discovery at publication time. Repository ownership improves code review and version coupling. Many systems use both: reviewed source schemas in version control and registered immutable versions for runtime coordination.

## Failure Modes and Misconceptions

- **“It parsed, so it is correct.”** Parsing establishes syntax, not domain meaning, range, unit or provenance.
- **“Optional means nullable.”** Absence of a property and a present null value are independent dimensions.
- **“Null means unknown.”** It may mean withheld, not applicable, invalid, pending or something else; define it.
- **“A default fills missing data.”** It resolves a read or operation but cannot establish an observed historical value.
- **“Zero is a safe missing sentinel.”** Zero is often a valid measurement and contaminates aggregates.
- **“Empty string is basically null.”** It may be a valid present value and its conversion destroys source state.
- **“All integers round-trip through JSON.”** JSON implementations differ; large integers can lose exactness in binary64-based paths.
- **“Wider physical type means compatible meaning.”** A representation can widen while units, identity or constraints change incompatibly.
- **“Float is precise enough for money.”** Binary representation and repeated operations can violate exact decimal rules.
- **“More decimal digits means more accuracy.”** Precision, scale, measurement uncertainty and source accuracy are different concepts.
- **“NaN is just null for floats.”** NaN participates in floating semantics and may not serialize through JSON.
- **“A string is a string.”** Encoding, normalization, case behavior, collation and domain grammar affect identity.
- **“Normalization is harmless cleanup.”** Compatibility forms can collapse distinctions; preserve originals when needed.
- **“A nullable list covers null elements.”** Container validity and element validity are separate.
- **“Unknown enum can map to the first member.”** That asserts a domain meaning the producer did not send.
- **“Inference found the schema.”** It found a hypothesis from a bounded sample and heuristic.
- **“Permissive casting improves quality.”** It may only move failures downstream while concealing producer drift.
- **“Renaming a column is metadata-only.”** Name-resolved systems may interpret it as delete-and-add.
- **“Unused field numbers are reusable.”** Historical bytes can then decode with a false new meaning.
- **“Registry compatibility proves safety.”** It covers configured structural rules, not every deployed consumer or domain invariant.
- **“Additive changes are always safe.”** New fields may alter authorization, billing or behavior even if old readers ignore them.
- **“Null-rate stability proves quality.”** A producer can replace real observations with repeated defaults while null rate falls.
- **“Quarantine means data loss.”** Proper quarantine preserves evidence and prevents invalid data from entering trusted products.
- **“Round trip means printed strings match.”** Formatting can hide precision, scale, normalization and presence loss.

## Worked Examples

### Example 1

A promotion feed supplies four `discount_percent` records: property absent, property explicitly null, numeric zero and empty string. The contract says absence means the producer does not support the field, null means it supports the field but has no value, zero is a valid no-discount observation, and empty string is invalid.

The ingestion state is therefore `Missing`, `Null`, `Present(0)` and `Invalid(empty-string)`. A report may display all first three as blank or zero, but storage retains the state. The invalid record is quarantined with source offset and reason. A later default of zero is tagged as derived rather than observed.

### Example 2

An event carries account ID `9007199254740993`, which is $2^{53}+1$. The source uses a 64-bit integer and the JSON gateway feeds a consumer whose number model cannot represent that integer exactly. The consumer sees a neighboring value, so syntax succeeded but identity failed.

The contract changes the JSON representation to a decimal digit string with a grammar that forbids signs, exponent notation and unwanted leading-zero normalization. Binary/internal systems may retain unsigned or signed 64-bit storage if their range is checked. Fixtures test the boundary around $2^{53}$ and the maximum permitted account ID.

### Example 3

A payment amount is `12.30 USD`. Storing it as binary float risks base-2 approximation; storing `1230` without scale or currency is also incomplete. The field contract uses decimal precision 12, scale 2, currency `USD`, with half-even rounding only at a named settlement operation.

The Parquet representation carries a decimal logical annotation, not just an integer. A mapping validator rejects scale 3 unless the source operation explicitly rounds. It tests maximum magnitude, negative adjustments, `0.00`, and halfway values. Export preserves two fractional digits because this domain treats scale as part of the contractual representation.

### Example 4

A sensor stream uses binary64 measurements and can produce NaN when the device algorithm cannot compute a value. JSON export has no standard NaN number token. The team first considered converting NaN to null, but null already means the sensor did not report.

The chosen schema uses a tagged result: `measurement` for finite values and `quality_code` for `not_reported`, `not_computable` or `out_of_range`. Raw binary data retains the original floating payload for authorized diagnosis. The export rejects infinities and separately counts each quality state.

### Example 5

Two customer keys look like “Café”; one uses a composed `é`, the other `e` plus combining acute. Raw UTF-8 bytes differ, so a byte-keyed join misses the match. The identity contract derives an NFC-normalized match key while preserving the entered display string.

The team does not apply compatibility normalization or locale-dependent lowercasing without a domain decision. Tests include composed/decomposed forms, Turkish case behavior, combining marks and scripts used by customers. The schema versions the normalization algorithm and Unicode data version used for keys.

### Example 6

Consider an optional `readings` field whose value is a nullable list of nullable integers. Missing field means the device firmware predates readings. A null list means the device supports readings but the sampling operation failed. An empty list means sampling succeeded with no observations. `[1,null,3]` means the middle observation is absent.

Four fixtures cross the Arrow, Parquet and query-engine path. The physical layouts may use separate definition levels or validity bitmaps, but the end consumer must reconstruct all four states. If a target binding cannot express them, the schema adds an explicit state tag before that hop.

### Example 7

An old shipping consumer knows `PENDING`, `IN_TRANSIT` and `DELIVERED`. A new producer adds `CUSTOMS_HOLD`. Mapping the unknown member to `PENDING` would misstate operational status.

The wire representation preserves the unknown numeric identity, and the application exposes `Unrecognized(code)` while retaining raw bytes. UI can display “status unavailable” and telemetry records the unknown. The field number and retired enum numbers are reserved; a consumer-first rollout teaches readers before writers emit the new member.

### Example 8

A CSV inference sample contains account codes `1001`, `1002` and `1003`, so the tool proposes integer. A later partition contains `001004` and `A1005`. Integer parsing would erase leading zeros and quarantine the lettered code after curated data already exists.

The inference result is treated as provisional evidence. Domain ownership establishes a constrained string type. Raw files remain immutable, the candidate schema records its sample digest, and the curated rebuild uses the approved contract. Monitoring reports lexical-pattern drift without converting the identifiers to quantities.

### Example 9

A table field named `surname` with stable ID 17 becomes `family_name`. An ID-aware table format records a rename, so old files and new files resolve to the same field. A downstream CSV export is name-based and requires an alias window.

The plan deploys readers accepting both names, updates the canonical writer, monitors old-name use, then retires the alias. ID 17 remains unchanged. If the field were dropped, ID 17 would be retired permanently rather than reused for a different concept.

### Example 10

A clinical dataset has a `diagnosis` field. Null formerly mixed three states: not assessed, assessed with no diagnosis, and diagnosis redacted for the recipient. Analysts incorrectly counted all nulls as not assessed.

The revised contract adds a required `diagnosis_state` enum and permits `diagnosis_value` only for `present`. Authorization derives `redacted` during export, preserving an audit event without exposing the value. Migration labels legacy nulls `legacy_unknown` rather than inventing certainty. Metrics and queries group by state before interpreting the value column.

## Cross-Program Connections

**API and Service Engineering.** Request/response schemas must distinguish omitted patch fields from explicit clear operations, preserve unknown enum values and coordinate generated clients across versions. The compatibility matrix developed here applies directly to service rollout.

**Database Engineering.** SQL null semantics, constraints, numeric types, collations and transactional enforcement determine how a logical contract behaves after persistence. Database DDL is one implementation of the domain schema, not necessarily its complete definition.

**Domain-Driven Design and Modeling.** Value objects make units, identity and invariants explicit. An `AccountId`, `Money` or `DiagnosisState` prevents unrelated primitives from being treated as interchangeable merely because their storage types match.

**Programming Languages.** Option types, tagged unions, arbitrary-precision integers, decimal libraries and generated bindings differ in expressiveness. A cross-language boundary must map the contract rather than assume native types coincide.

**Security Engineering.** Validation constrains hostile inputs; overflow and allocation limits protect availability; redaction states preserve policy intent; and error telemetry must avoid leaking sensitive values. Unknown-field behavior can also affect signed or authorized payloads.

**Distributed Systems.** Mixed-version readers and writers make schema evolution a distributed protocol. Retained logs, replay, retry and disaster recovery extend the compatibility horizon beyond the ordinary deployment window.

**Machine Learning Engineering.** Missingness mechanisms, defaults and invalid-value coercion affect feature distributions and model behavior. A stable primitive type does not prevent semantic drift; state-rate and unit telemetry are necessary inputs to model monitoring.

**Systems Engineering.** Type fidelity is an interface invariant spanning organizational boundaries. Hazard analysis asks what happens when a plausible but false value reaches a decision, not only whether a decoder returned success.

## References

1. IETF, [RFC 8259: The JavaScript Object Notation Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259.html), retrieved 2026-09-02.
2. JSON Schema, [Draft 2020-12 Core](https://json-schema.org/draft/2020-12/json-schema-core.html) and [Validation Vocabulary](https://json-schema.org/draft/2020-12/json-schema-validation.html), retrieved 2026-09-02.
3. Apache Avro, [Specification 1.12.0](https://avro.apache.org/docs/1.12.0/specification/), retrieved 2026-09-02.
4. Protocol Buffers, [Application Note: Field Presence](https://protobuf.dev/programming-guides/field_presence/), retrieved 2026-09-02.
5. Apache Arrow, [Columnar Format](https://arrow.apache.org/docs/format/Columnar.html), retrieved 2026-09-02.
6. Apache Parquet, [Logical Type Definitions](https://parquet.apache.org/docs/file-format/types/logicaltypes/), retrieved 2026-09-02.
7. Unicode Consortium, [Unicode Standard Annex #15: Unicode Normalization Forms](https://www.unicode.org/reports/tr15/), retrieved 2026-09-02.
8. Apache Iceberg, [Table Specification](https://iceberg.apache.org/spec/), retrieved 2026-09-02.
9. IEEE Standards Association, [IEEE 754-2019: Standard for Floating-Point Arithmetic](https://standards.ieee.org/ieee/754/6210/), retrieved 2026-09-02.

## Exercises

### Exercise 1

An update endpoint receives five payloads for `credit_limit`: property absent, null, `0`, `"0"` and `""`. Domain rules say absent means unchanged, null means clear the limit, integer zero is valid, numeric strings may be accepted only by a documented legacy adapter, and empty string is invalid. Design a state/conversion table, failure behavior and telemetry. Explain why applying a zero default before classification is unsafe.

### Exercise 2

A pipeline maps signed 64-bit order IDs through JSON, a binary64-only scripting client and a signed 32-bit database column. Construct a fidelity matrix for `-1`, `0`, $2^{31}-1$, $2^{31}$, $2^{53}-1$, $2^{53}$ and $2^{53}+1$. Propose a representation that preserves the allowed domain of nonnegative signed-64-bit IDs, including lexical constraints.

### Exercise 3

Design a schema for an optional `measurements` field. The field may be unsupported, collection may fail, collection may succeed with no samples, and individual samples may be missing or present decimal values with unit `mg/L`, precision 8 and scale 3. State container and element nullability, tags, constraints and at least eight round-trip fixtures.

### Exercise 4

Version 1 has field ID 4 named `price`, decimal(10,2), required. Version 2 wants the name `unit_price`, decimal(14,4), and a new optional currency. Plan reader/writer rollout, compatibility tests, default/backfill policy, field identities, boundary cases, rollback and telemetry. Identify what is structurally compatible versus what still requires domain approval.

### Exercise 5

A health-data export currently uses null for not collected, not applicable and policy-redacted values. Design a migration that restores useful distinctions without inventing historical facts. Include schema, legacy labeling, authorization, validation, aggregate metrics, privacy protections, consumer rollout and evidence needed before declaring completion.

## Answers to the Exercises

### Answer 1

Classify before resolution. Map absent to `Missing/unchanged`, explicit null to `Null/clear`, integer zero to `Present(0)/set`, string `"0"` to `LegacyLexical` and then exact integer zero only inside the named adapter, and empty string to `Invalid` with quarantine or a 4xx response. Preserve the original payload or authorized digest, producer/version, reason and adapter version.

Count each source state, adapter coercions, rejections and resulting command. Alert on changes by producer. Applying zero first maps absent and explicit zero to one value, so the service can no longer tell “leave unchanged” from “set zero.” In a patch this can overwrite valid state. Explicit null must remain a distinct clear command.

### Answer 2

The 32-bit target accepts `-1`, `0` and $2^{31}-1$ physically, but the nonnegative ID domain rejects `-1`. It rejects all larger cases. A binary64 client represents integers exactly through $2^{53}$, while $2^{53}+1$ cannot be preserved as a distinct value; RFC guidance uses the conservative interoperable interval ending at $2^{53}-1$. Thus neither current hop covers the full allowed signed-64-bit nonnegative domain.

Represent IDs in JSON as strings matching either `0` or a nonzero digit followed by digits, with no sign, whitespace, decimal point, exponent or leading zeros. Parse directly into a checked 64-bit integer or keep a domain string. Widen the database column to a representation covering `0` through $2^{63}-1$. Test every listed value plus $2^{63}-1$, $2^{63}$, leading zeros, signs and exponent notation end to end.

### Answer 3

Use a tagged outer state such as `unsupported`, `collection_failed` or `collected`, rather than overloading null. When `collected`, require a non-null list; empty list means success with no samples. Each element is a tagged `missing(reason)` or `present(value)`. Present values use exact decimal(8,3) and unit `mg/L`; validate magnitude, scale and permitted sign.

Fixtures include missing legacy field/unsupported, explicit unsupported, collection failure with reason, collected empty list, one present `0.000`, maximum positive, maximum negative if permitted, one missing element, mixed present/missing elements, excessive scale, excessive magnitude and wrong unit. The last three must reject or quarantine. Round-trip all accepted states through memory, file, query and export representations.

### Answer 4

Keep field ID 4 for the rename and add a new stable ID for currency. Deploy readers that accept old decimal(10,2) and new decimal(14,4), preserve scale semantics and accept absent currency before new writers. Then canary writers with the renamed schema and currency. Test old/new readers against old/new files, recovery tools, maximum magnitudes, negative values, rescaling and rounding boundaries.

Wider precision/scale may be structurally representable but changes allowed values and rounding expectations; domain owners must approve. Currency cannot be guessed historically. Use an absent/unknown state or a provenance-bearing backfill from reliable evidence, not an unmarked default. Rollback keeps readers dual-capable and stops new emission; it cannot safely send values exceeding the old range to old writers. Monitor schema versions, decimal rescaling, overflow, absent currency and consumer errors.

### Answer 5

Add a required state field with `present`, `not_collected`, `not_applicable`, `redacted` and `legacy_unknown`; allow the sensitive value only for `present`. Export derives `redacted` after authorization and records an audit event without exposing the original. Validate forbidden combinations such as `redacted` plus visible value.

Migrate historical null to `legacy_unknown` unless independent evidence proves a more specific state. Deploy consumers that understand the state before changing writers. Report aggregate state counts, legacy share, invalid combinations and policy version while suppressing small groups and sensitive raw values. Retain access-controlled lineage and sample-based reconciliation. Completion requires compatibility tests, authorization tests, privacy review, stable metrics and evidence that downstream analyses no longer interpret every absent value as not collected.
