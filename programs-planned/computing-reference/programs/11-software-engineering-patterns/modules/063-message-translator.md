---
module_id: SEPAT-063
program: Software Engineering: Patterns
level: 2
module_number: 63
title: Message Translator
status: complete
last_verified: 2026-08-29
---

# Message Translator

## One-Page Review

### Governing question

How can systems exchange semantically equivalent messages across different schemas, encodings, units, identifiers, and domain vocabularies while making validation, provenance, precision, loss, defaults, compatibility, replay, security, and failure explicit?

### Essential definitions

- A **Message Translator** converts a message from one representation into another so otherwise incompatible systems can communicate.
- A **source schema** and **target schema** define structural contracts; a **semantic mapping** defines how meanings correspond.
- **marshalling/serialization** changes in-memory data to a wire encoding; it is not necessarily domain translation.
- A **Normalizer** maps several source formats into one common representation; a **Canonical Data Model** is the shared target vocabulary.
- A **lossless translation** preserves all in-scope distinctions needed to reconstruct an equivalent source; a **lossy translation** intentionally merges or omits distinctions and records that policy.
- **presence** distinguishes missing, explicit null, default, empty, zero, false, unknown, and redacted states.
- A **mapping version** immutably identifies source/target schema versions, semantic rules, reference data, and code/config used.
- **translation provenance** links source identity/digest, translator/mapping version, target identity, time, and outcome.
- A **compatibility window** is the set of deployed/historical source and target versions that must interoperate.
- A **translation error taxonomy** distinguishes malformed, unsupported version, semantic invalidity, ambiguous/lossy mapping, unauthorized data, and infrastructure failure.

### Central model, mechanism, or theorem

Let \(S_v\) and \(T_w\) be valid source and target semantic domains for schema versions \(v,w\). A versioned translator is a partial function

\[
\tau_{v,w,k}:S_v\rightharpoonup T_w,
\]

where \(k\) fixes mapping/reference-data version. It returns either a target plus provenance/loss report or a typed rejection. Structural validation alone proves only membership in a schema, not that \(\tau\) preserves meaning.

For a declared lossless subset \(S^*\subseteq S_v\), an independently implemented inverse/decoder \(\rho\) should satisfy semantic round-trip:

\[
\forall s\in S^*,\quad \rho(\tau(s))\equiv_S s.
\]

If two semantically distinct source values map to one target,

\[
s_1\not\equiv_S s_2\land\tau(s_1)=\tau(s_2),

\]

then translation is non-injective and loses that distinction. The loss must be acceptable, named, measured, and irreversible claims prohibited.

### Critical invariants

- Source bytes/envelope are authenticated, size-bounded, safely parsed, and validated before semantic access.
- Source and target schema/type/version are explicit; unknown versions never silently use a “close enough” mapper.
- Mapping preserves stated business meaning, identity lineage, causation, tenant, time semantics, units, currency, precision, and ordering—or records intentional loss.
- Missing, null, default, empty, unknown, redacted, and invalid remain distinct according to both contracts.
- Numeric/unit/time/encoding conversions define ranges, rounding, overflow, locale, calendars, zones, and normalization.
- Translation is deterministic for the same source and mapping/reference versions; mutable enrichment is separate or captured.
- Target is validated after mapping and cross-field/domain invariants are checked by an authoritative policy owner.
- Errors do not acknowledge/discard important input until durable quarantine/retry/evidence policy is satisfied.
- Sensitive fields are minimized/redacted under current authorization; translator logs and quarantine do not leak payload.
- Compatibility, replay, backfill, dual-running, reconciliation, rollback/forward, and mapping retirement are tested across retained history.

### Common failures

Common failures include renaming fields without mapping meaning, wire compatibility mistaken for semantic compatibility, float conversion of money, implicit locale/time zone, null collapsed with missing, unknown enum mapped to ordinary default, regenerated identifiers, altered event time, unordered map/list assumptions, Unicode corruption, silent truncation, unit overflow, applying today's lookup table during historical replay, translator performing remote enrichment invisibly, schema-valid but domain-invalid targets, dead letters with raw personal data, point-to-point translator explosion, untested old messages, and assuming round-trip because both directions compile.

### Compact example

A pure `invoice-v1` to `invoice-v2` translator converts integer minor units to an exact two-decimal string, preserves invoice/message identity and currency, binds mapping version `invoice-map-3`, and rejects missing currency. Two valid messages translate without mutating inputs; one invalid input yields a typed error.

### Connections

[SEPAT-062](062-message-router.md) chooses destinations without changing meaning; [SEPAT-064](../ROADMAP.md) introduces a Canonical Data Model as a shared translation vocabulary. Translation also connects to [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md), [Database Engineering](../../18-database-engineering/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

What evidence shows that a translated message means what the source meant—not merely that the target parser accepts it—and how should unavoidable ambiguity, loss, evolution, and failure be governed?

Translation sits at a semantic boundary. The source may say `amount=12345`, the target may expect `123.45`, and both can be syntactically valid while disagreeing by two orders of magnitude. Correctness lives in explicit vocabulary, units, invariants, provenance, and reviewed mapping rules.

## Why This Matters

Independent systems evolve representations for their own domains. Messaging requires them to communicate without forcing one internal model on all participants. A translator localizes incompatibility and protects endpoints from foreign schemas.

The risk is silent corruption. Translation often succeeds technically while losing precision, identity, status distinctions, timestamps, or authority. Such defects propagate asynchronously and may be replayed years later. A production translator is governed data logic, not glue code.

## Prerequisites and Retrieval

You should understand Message Channel, Message Router, schemas/types, serialization, algebraic data types, identity/provenance, decimal arithmetic, time/Unicode, validation, authorization/privacy, version deployment, property testing, and reconciliation. Retrieve these facts:

1. Parsing proves an encoding can be interpreted; schema validation proves structural constraints; neither proves business semantics.
2. Adding/removing fields can be wire-compatible while changing defaults or meaning for old/new consumers.
3. Binary floating point cannot exactly represent many decimal fractions; money generally needs decimal or integer-minor-unit policy.
4. A timestamp without offset/zone/calendar/precision may be ambiguous; local civil time can be missing or repeated.
5. Unknown enum values support forward compatibility only if consumers preserve or govern them safely.
6. Unicode strings can have visually equivalent but byte-distinct forms; normalization can change identifiers/signatures.
7. Historical replay using mutable current lookup data may produce a different target than original processing.

## Learning Objectives

After completing this module, you should be able to:

- distinguish semantic translation from serialization, adapters, enrichment, routing, normalization, and canonical modeling;
- specify a partial versioned mapping with typed errors, provenance, and declared information loss;
- map identity, presence, enumerations, money, units, time, text, collections, and nested structures safely;
- reason about injectivity, semantic round trips, invariants, and counterexamples;
- design deterministic translation and isolate/version mutable reference-data enrichment;
- validate and authorize source/target while preventing parser, injection, tenant, and privacy failures;
- evolve mappings across producer/consumer overlap, retained messages, replay, backfill, and retirement;
- compare pairwise translators, normalizers/canonical models, consumer-owned mapping, and schema evolution;
- verify with golden, property, metamorphic, differential, mutation, fault, security, and reconciliation evidence;
- construct named human review for high-stakes financial, clinical, safety, or regulated semantics.

## Core Exposition

### Start with two semantic contracts

Document source and target field meaning, owner, lifecycle, units, allowed ranges, presence, invariants, identity, time, authority, privacy classification, and evolution. A field-name table is insufficient. Include examples and counterexamples in domain language.

Map one named source version to one named target version under one mapping/reference version. Avoid `latest` at runtime. A dispatcher may select a versioned translator, but unsupported combinations yield explicit errors.

### Separate decoding, translation, and encoding

Pipeline stages are: authenticate/size-limit; decode wire bytes; validate source shape; construct a typed semantic source; translate; validate target shape and invariants; encode; durably publish. Each stage has its own error category and evidence.

Marshal/unmarshal changes representation such as JSON to object or object to Avro. Translation changes vocabulary/model. Keeping them distinct prevents parser defaults/coercions from becoming hidden business mappings.

### Treat the translator as a partial function

Not every syntactically valid source has a meaningful target. Reject unsupported source versions, unknown required enums, out-of-range values, contradictory states, ambiguous identifiers, and target-unrepresentable precision. A typed rejection is safer than invention.

Totality should mean every admitted input receives success or a governed error, not that every input is coerced into a target.

### Preserve identity and lineage

Keep original message/event/domain identity according to contract. A translated envelope may receive a derived transport ID, but provenance links source ID/digest, mapping version, translator, target ID, causation/correlation, tenant, and timestamps. Do not generate a new business identity that makes duplicates look distinct.

If target identity namespace differs, use a deterministic, collision-resistant mapping table or namespaced composite and define lifecycle/reuse. Hashes are not inherently privacy-safe identifiers.

### Make presence explicit

Create a mapping table for source missing/null/default/empty/zero/false/unknown/redacted/invalid to target states. If target cannot distinguish them, record loss or reject when distinction matters. Do not let deserializer-generated defaults erase source presence before mapping.

When adding a target required field, derive it only from authoritative source/reference premises. An arbitrary constant may make schema validation green while corrupting meaning.

### Map enumerations without unsafe defaults

Map each known source enum to a target value with meaning evidence. Preserve unknown raw code/provenance where target supports an `unknown(code)` alternative; otherwise quarantine or route to reviewed fallback. Never map unknown status to `ACTIVE`, `NORMAL`, or another actionable ordinary state.

Merging several source statuses is lossy. Document why target does not need the distinction and how reverse/reconciliation/audit works.

### Convert money exactly

Carry amount plus ISO currency and unit/scale. Convert integer minor units or decimal using exact arithmetic. Define rounding mode, application point, permitted scale, min/max, overflow, negative/zero, tax/discount composition, and currency exponent/version.

Never infer currency from locale or tenant without versioned authoritative policy. Do not round each line when contract rounds aggregate, or vice versa. Recompute and reconcile totals under named policy.

### Convert physical units dimensionally

Represent value, unit, dimension, precision/uncertainty, and measurement context. Use exact rational/decimal factors where applicable and test boundary/overflow. Temperature conversions require offsets; dosage may require patient context and cannot be a blind unit multiplier.

Reject dimension mismatch. A field named `weight` does not identify kilograms versus pounds or measured versus estimated.

### Preserve time semantics

Distinguish event occurrence, recording, processing, effective interval, and local scheduled time. Preserve UTC instant with offset/zone/provenance when available; a zone ID carries future/historical daylight rules, while an offset alone does not.

Define precision/truncation, leap-second/calendar policy, ambiguous/nonexistent local time, inclusive/exclusive interval bounds, and clock uncertainty. Do not replace source occurrence time with translator processing time.

### Handle text and encodings deliberately

Decode with declared charset and reject invalid sequences according to policy. Unicode normalization, case folding, whitespace trimming, transliteration, and locale-sensitive collation are semantic transformations; apply only to fields whose contract permits them.

Preserve original display text separately from normalized search/key values. Never normalize signed bytes before signature verification. Bound lengths and expansion to prevent memory/decompression/normalization denial of service.

### Map collections and graphs

Define whether list order, duplicates, identity, null elements, and partial pages matter. Mapping a list to a set loses order/duplicates; flattening nested values can create key collisions; recursively translating cyclic/deep graphs needs depth/size bounds.

For split targets, derive child identities deterministically and include sequence/cardinality/correlation. Partial translation must not masquerade as a complete target aggregate.

### Distinguish translation from enrichment

Pure translation uses source plus immutable mapping/reference version. Enrichment fetches missing data from another source and introduces availability, authorization, snapshot, freshness, cache, and replay semantics. Model it as an explicit Content Enricher or application workflow.

If mapping needs a code table, bind an immutable table version/digest in provenance. “Current exchange rate” or “current customer tier” makes historical replay nondeterministic and may be a business decision rather than translation.

### Validate target meaning

After constructing the target, validate target schema and cross-field invariants: totals, lifecycle combinations, reference namespaces, required provenance, temporal order, tenant consistency, and information-classification constraints. Target validation errors are mapping defects or unrepresentable sources, not producer syntax errors.

Use database/consumer constraints as defense in depth. The translator cannot claim downstream acceptance/effect merely because encoding succeeds.

### Declare and measure information loss

Maintain a loss ledger per mapping: omitted fields, merged enums, reduced precision, truncated text/time, ordering/duplicate loss, redaction, and defaulted data. Classify mandatory/acceptable/conditional/forbidden loss and expose counts.

For lossless claims, test independently implemented round trips over a declared subset and semantic equivalence—not byte equality unless canonical encoding is guaranteed. For lossy mappings, test equivalence of the properties promised to remain.

### Version mappings immutably

Version includes source schema, target schema, semantic rules/code, reference tables, rounding/time policies, and dependency versions that affect output. Store build/checksum and effective dates. Do not edit an old version in place; retained inputs/provenance must remain reproducible.

Mapping selection comes from trusted envelope/type registry, never heuristic guessing by field presence alone. Content sniffing can be ambiguous and insecure.

### Evolve across deployment overlap

List the compatibility matrix: old/new producers, translator versions, old/new target consumers, stored/replayed messages. Prefer additive changes and tolerant readers only where unknown/default semantics are safe. Wire-safe and semantic-safe are distinct reviews.

For breaking evolution, add a new message type/version and translator, dual-read or dual-publish only with one authoritative decision/effect and reconciliation, canary, then retire after retention/drain evidence. Reserve removed field identifiers/names where the serialization technology requires it.

### Govern replay and backfill

Replay may reproduce the original target using original mapping/reference versions, or intentionally remap history under a new policy. Name the operation. The latter creates new derived data/effects and needs new operation identity, authorization, scope, comparison, and rollback.

Rate-limit, checkpoint, deduplicate, shadow compare, and reconcile counts/amounts/identities. Never replay irreversible commands merely to test a translator.

### Handle errors without losing input

Classify decode, source-schema, unsupported-version, semantic, authorization/privacy, mapping, target-schema, encoding, infrastructure, and publish errors. Permanent bad input goes to owned access-controlled quarantine with minimal protected evidence; transient infrastructure retries within budget.

Do not log raw payload or stack traces containing secrets/personal data. Provide authorized tooling to inspect/redact/correct/reprocess while preserving original immutable evidence and new attempt identity.

### Secure the translation boundary

Authenticate source/channel, authorize type/tenant/purpose, validate integrity before parsing, enforce size/depth/count limits, use safe parsers, disable dangerous polymorphic/object construction, and protect against injection/formula/entity/deserialization attacks. Treat target strings as data and parameterize downstream usage.

Apply field-level disclosure/minimization and current policy. A translator cannot make unauthorized sensitive input permissible by renaming it. Encrypt at rest/in transit, rotate keys, and protect mappings/reference data/control plane from tampering.

### Observe translation quality

Metrics include source/target/mapping versions from bounded sets, success/error category, latency, bytes/records, loss category/count, unknown enum, default/redaction/truncation/rounding, quarantine age, replay/backfill progress, output publish, and reconciliation mismatch. Avoid message IDs, tenant IDs, raw codes, or payload values as metric labels.

Trace source-to-target lineage and log protected digests/IDs according to privacy policy. Alert on new version, default/loss spike, drift, overflow, validation failure, and mapping-version skew.

### Test at several evidence layers

Golden examples from domain owners anchor intended meaning but do not cover boundaries. Add property/metamorphic tests for round trips, scale/unit identities, order/duplicate preservation, presence, invariants, and deterministic replay; mutation tests ensure wrong mappings fail; differential tests compare old/new or independent implementations.

Fuzz parser/schema/translator with size/depth/encoding/unknown fields. Test all compatibility pairs and historical fixtures. Integration-test real serializers/registries/broker/database, auth/privacy, quarantine/redrive, failure before/after input ack/output publish, and rolling deployment. Load-test representative/adversarial size and reference-data skew. Reconcile source and target identities, counts, money totals, statuses, and loss ledger.

### Control pairwise translator growth

With \(n\) formats, direct bidirectional pairs can approach \(n(n-1)\) mappings. A canonical model can reduce edges toward \(2n\), but only by creating a governed shared semantic contract and possible loss at its boundaries. It can become an enterprise bottleneck or lowest-common-denominator model.

Use canonical models within coherent domains, not automatically across an organization. Sometimes consumer-owned anti-corruption translation or compatible schema evolution is simpler.

### Review high-stakes semantics with humans

Financial, clinical, safety, scientific, legal, and identity translations require named experts to validate units, terminology/code systems, presence/unknown meaning, precision, time, identity, provenance, and failure workflow. Include affected users and accessibility/human-factors for operator review tools.

Automated schema and property tests establish encoded rules, not substantive correctness or regulatory compliance.

### Executable model: exact invoice amount translation

This finite pure translator maps an integer minor-unit amount to an exact two-decimal string, preserves source identities/currency, binds a mapping version, rejects absent currency, and does not mutate inputs. It assumes currencies with two minor digits and therefore is not a universal currency converter.

<!-- bijux-verify: {"id":"message-translator-invoice","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"msg-1 status=translated amount=123.45 currency=EUR mapping=invoice-map-3 preserved=True\nmsg-2 status=translated amount=0.00 currency=USD mapping=invoice-map-3 preserved=True\nmsg-3 status=invalid reason=missing-currency preserved=True\n","stderr":""}} -->
```python
MAPPING_VERSION = "invoice-map-3"


def decimal_text(minor_units):
    sign = "-" if minor_units < 0 else ""
    absolute = -minor_units if minor_units < 0 else minor_units
    return f"{sign}{absolute // 100}.{absolute % 100:02d}"


def translate(source):
    if "currency" not in source:
        return {"status": "invalid", "reason": "missing-currency"}
    target = {
        "status": "translated",
        "message_id": source["message_id"],
        "invoice_id": source["invoice_id"],
        "amount": decimal_text(source["amount_minor"]),
        "currency": source["currency"],
        "mapping": MAPPING_VERSION,
    }
    return target


sources = [
    {"message_id": "msg-1", "invoice_id": "inv-7", "amount_minor": 12345, "currency": "EUR"},
    {"message_id": "msg-2", "invoice_id": "inv-8", "amount_minor": 0, "currency": "USD"},
    {"message_id": "msg-3", "invoice_id": "inv-9", "amount_minor": 50},
]

snapshots = [repr(source) for source in sources]
for index, source in enumerate(sources):
    target = translate(source)
    preserved = repr(source) == snapshots[index]
    if target["status"] == "translated":
        print(f"{source['message_id']} status=translated amount={target['amount']} currency={target['currency']} mapping={target['mapping']} preserved={preserved}")
    else:
        print(f"{source['message_id']} status=invalid reason={target['reason']} preserved={preserved}")
```

### Finite invariant argument

For `12345`, integer division yields 123 and remainder 45, producing `123.45`; for zero both components are zero and two-digit formatting produces `0.00`. Both valid paths copy message/invoice identity and currency and attach `invoice-map-3`. The third source lacks the key, so it returns before accessing/converting amount and reports `missing-currency`.

Functions only read source dictionaries and construct new strings/dictionaries. The loop only reads, so each source representation equals its snapshot. Exact line order follows source list order. This proves only the finite serialized trace. It assumes integer inputs, two-digit currency scale, required IDs, safe sizes, and Python integer behavior; production mapping must validate types/ranges/currency scale, schemas, authorization, provenance, publication, and failures.

### Evidence classification

The snippet report is empirical evidence for two exact conversions, one typed rejection, mapping label, and modeled input preservation. Arithmetic/branch outcomes are independently recomputable. It provides no schema registry, serializer, broker, transaction, authorization, privacy, broad currency, performance, or domain-review evidence.

## Definitions and Notation

Let decoded source \(s\in S_v\) and target \(t\in T_w\). Mapping context \(k=(mapping,reference,rounding,time,code\text{-}system\ versions)\) is immutable for deterministic \(\tau_{v,w,k}\). Result type is

\[
Result(t,provenance,loss)\;|\;Reject(category,evidence,retryability).
\]

Semantic equivalence \(\equiv_S\) compares source meaning rather than bytes or object identity. Injectivity on a subset means \(\tau(s_1)=\tau(s_2)\Rightarrow s_1\equiv_S s_2\). A round-trip test needs an independently credible \(\rho\); using the same erroneous mapping table both ways can falsely pass.

Presence domain may be \(P(V)=Missing|Null|Present(V)|Unknown(code)|Redacted(reason)|Invalid(reason)\). Target mapping must state which distinctions remain. Loss ledger \(L_k\) lists each merged/omitted/truncated/rounded/redacted distinction and its policy.

Provenance record \(p=(source\_id,source\_digest,v,w,k,target\_id,time,outcome,loss\_digest)\) supports audit/replay while payload access remains separately protected.

## Mechanisms, Invariants, or Proof Structure

The mechanism is a staged transducer:

1. Authenticate, authorize, integrity-check, and bound the envelope/bytes.
2. Decode with an explicit format version and safe parser.
3. Validate source schema, presence, and domain preconditions.
4. Apply pure versioned semantic mapping and produce loss/provenance.
5. Validate target schema and semantic invariants.
6. Encode under a named wire format/version.
7. Durably store/publish target and provenance or quarantine typed failure.
8. Reconcile source, decisions, target, downstream effects, and loss metrics.

Core invariants are explicit version selection; stable identity/tenant/causation lineage; exact declared unit/precision/time conversion; presence/unknown preservation or governed loss; deterministic output for fixed \((s,k)\); no unauthorized field expansion; target validity; no acknowledgement before recoverable target/error outcome; immutable provenance; and reproducibility for retained supported history.

Proof obligations divide by claim. Structural validators establish schema membership. Arithmetic/dimensional proofs and independent recomputation establish conversions on bounded domains. Round-trip/injectivity tests find loss on declared subsets. Property/fuzz/mutation tests explore large domains but are not exhaustive. Compatibility matrices and historical differential runs establish deployment/replay evidence. Domain, privacy, safety, and regulatory experts validate semantics that code cannot derive.

## Alternatives and Trade-Offs

| Approach | Mapping owner | Strong fit | Main risk |
|---|---|---|---|
| Pairwise translator | Integration boundary | Few stable formats | \(O(n^2)\) mapping sprawl |
| Canonical Data Model | Shared domain governance | Many integrations in coherent domain | Central coupling/semantic flattening |
| Consumer anti-corruption layer | Consumer | Protect local domain model | Duplicate interpretations |
| Producer emits consumer format | Producer | One strategic consumer | Producer coupling/data leakage |
| Compatible schema evolution | Contract owners | Same semantic message lineage | Wire-safe but semantic drift |
| Content Enricher | Workflow/integration | Missing authoritative data | Availability/snapshot/replay cost |
| Shared database/view | Data owners | Controlled analytics/legacy | Ownership/schema/security coupling |

Serialization libraries and mapping generators reduce mechanical code but cannot infer semantic equivalence, loss acceptability, authorization, or correct units.

## Failure Modes and Misconceptions

- **“Both schemas validate, so translation is correct.”** Structural membership does not prove meaning.
- **“Translation is renaming fields.”** Units, presence, identity, lifecycle, time, and vocabulary may differ.
- **“Wire-compatible means semantically compatible.”** Defaults and meaning can change without parser failure.
- **“Unknown enum maps to default.”** This can turn unsupported state into ordinary/actionable state.
- **“JSON number is a number.”** Precision/range/scale differ across runtimes and contracts.
- **“UTC fixes all time.”** Local schedules, zones, intervals, precision, and occurrence versus processing still matter.
- **“Normalize every string.”** It can change identifiers, signatures, display text, and legal meaning.
- **“Round trip proves lossless.”** Shared bugs and weak equivalence can make both directions wrong.
- **“Enrichment is translation.”** External lookup adds freshness, failure, authorization, and replay semantics.
- **“Use current mappings for replay.”** It may produce different history and duplicate downstream effects.
- **“Canonical model removes translation.”** It moves translation to system/canonical boundaries and creates governance.
- **“Generate mappers and review less.”** Automation reproduces declared mappings, including wrong ones.
- **“Quarantine can store the raw payload.”** Privacy, secrets, retention, and access controls still apply.
- **“A new target ID is harmless.”** It can defeat dedupe, causation, correction, and audit lineage.
- **“Automated tests approve high-stakes semantics.”** Named experts must validate real mappings and failure policy.

## Worked Examples

### Example 1

**Situation.** Source amount `12345` means cents; target decimal `12345` is interpreted as dollars.

**Reasoning.** Both values pass numeric schemas but differ 100-fold. Map exact minor units with currency/scale and reconcile totals/boundaries.

**Conclusion.** Unit meaning is part of the contract.

### Example 2

**Situation.** Source distinguishes `PENDING_REVIEW` and `PENDING_CUSTOMER`; target has only `PENDING`.

**Reasoning.** Mapping is lossy and reverse cannot reconstruct responsibility. Accept only if target never acts on distinction and retain source status/provenance for audit, or extend target.

**Conclusion.** Enum merging requires explicit loss review.

### Example 3

**Situation.** Missing allergy list becomes an empty target array.

**Reasoning.** Unknown/unavailable becomes confirmed none—a high-stakes semantic error. Preserve knowledge state or reject/escalate.

**Conclusion.** Missing and empty are not interchangeable.

### Example 4

**Situation.** Local appointment `2026-10-25 02:30 Europe/Stockholm` is translated to an instant without disambiguation.

**Reasoning.** DST fall-back repeats that local time. Require offset/fold or authoritative scheduling rule and retain zone/provenance.

**Conclusion.** Civil time needs ambiguity policy.

### Example 5

**Situation.** Translator lowercases and Unicode-normalizes a signed account identifier.

**Reasoning.** Signature verification/digest and identity may change. Verify original bytes first; normalize only a separate contract-defined lookup key.

**Conclusion.** Text normalization is semantic and security-sensitive.

### Example 6

**Situation.** A replay converts old product codes using today's mutable catalog.

**Reasoning.** Output differs from original, defeating reproducibility. Bind historical code-table version or explicitly run a new remapping/backfill operation with comparison and new identity.

**Conclusion.** Reference-data version is part of mapping provenance.

### Example 7

**Situation.** A list of ordered dose administrations becomes a set of drug IDs.

**Reasoning.** Order, duplicates, dose/time, and identity vanish. This is not equivalent; create a purpose-built summary with declared loss rather than label it translation.

**Conclusion.** Collection shape encodes meaning.

### Example 8

**Situation.** New protobuf field reuses an old removed tag and historical bytes decode as sensitive new data.

**Reasoning.** Reserve removed field numbers/names and compatibility-test retained bytes; wire identifier reuse can corrupt or disclose data.

**Conclusion.** Schema evolution rules protect historical encodings.

### Example 9

**Situation.** Five systems require 20 directed pairwise mappings and change independently.

**Reasoning.** A bounded-domain canonical model can reduce edges, but must preserve meaningful distinctions and have governance/version ownership. Consumer anti-corruption may still suit specialized concepts.

**Conclusion.** Reduce translator sprawl without flattening the domain.

### Example 10

**Situation.** A clinical lab source reports `>500 mg/dL`; target accepts only a decimal value.

**Reasoning.** Converting to `500` changes a censored lower-bound observation into an exact measurement. Extend target with comparator/range and provenance or reject; obtain laboratory/clinical review.

**Conclusion.** High-stakes measurement qualifiers cannot be discarded for schema convenience.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) develops types, parsing, semantics, numeric representation, and program equivalence.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies schema migration, constraints, transactions, provenance storage, and reconciliation.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) develops contract/version compatibility, envelopes, idempotency, and consumer boundaries.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies safe parsing, authorization, injection defense, privacy, integrity, and key/control-plane protection.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) develops schema evolution, quality, lineage, backfill, and data-contract operations.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) provides property, mutation, differential, fuzz, compatibility, fault, and reconciliation evidence.
- [SEPAT-062](062-message-router.md) changes destination only; [SEPAT-064](../ROADMAP.md) studies a shared canonical semantic vocabulary.

## References

1. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003. Message Translator, Normalizer, Canonical Data Model, and related transformation patterns.
2. Enterprise Integration Patterns, [“Message Translator”](https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessageTranslator.html), accessed 2026-08-29. Pattern problem, solution, and relationships.
3. Apache Camel, [“Message Translator”](https://camel.apache.org/components/4.18.x/eips/message-translator.html), 4.18 LTS documentation accessed 2026-08-29. Bean and data-format translation mechanisms.
4. JSON Schema, [“JSON Schema Core, Draft 2020-12”](https://json-schema.org/draft/2020-12/json-schema-core), accessed 2026-08-29. JSON schema vocabulary and validation model.
5. Apache Avro, [“Specification”](https://avro.apache.org/docs/current/specification/), current specification accessed 2026-08-29. Schemas, binary encoding, names, defaults, and schema resolution.
6. Protocol Buffers, [“Language Guide (proto 3)”](https://protobuf.dev/programming-guides/proto3/), current guide accessed 2026-08-29. Field presence, unknown fields, reserved tags, and wire compatibility.
7. Unicode Consortium, [“Unicode Standard Annex #15: Unicode Normalization Forms”](https://unicode.org/reports/tr15/), current annex accessed 2026-08-29. Unicode normalization semantics.
8. IETF, [“Date and Time on the Internet: Timestamps”](https://www.rfc-editor.org/rfc/rfc3339), RFC 3339, 2002. Timestamp representation and offsets.
9. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Encoding/evolution, derived data, streams, and data-system correctness.
10. David Thomas and Andrew Hunt, *The Pragmatic Programmer*, 20th Anniversary ed., Addison-Wesley, 2019. Representation, invariants, and transformation pipelines.

## Exercises

### Exercise 1

Write a semantic mapping table from an order v1 schema to v2 covering identity, money, presence, enums, timestamps, lines/order, unknown fields, provenance, errors, and declared loss. State round-trip subset.

### Exercise 2

Prove or disprove losslessness for translations that (a) cents integer to two-decimal text, (b) ordered list to set, (c) five statuses to three, and (d) zoned local time to UTC instant. State assumptions and counterexamples.

### Exercise 3

Design a versioned translator needing country and currency reference data. Separate translation/enrichment, define snapshot/cache/outage/replay, authorization/privacy, rollout, observability, and reconciliation.

### Exercise 4

Plan migration from 30 pairwise translators to a bounded-domain canonical model without simultaneous rewrite. Cover semantic governance, compatibility, shadow/dual paths, authority, loss, rollback/forward, and retirement evidence.

### Exercise 5

Review translation of high-stakes clinical lab results between code systems. Cover identifiers, code/version, values/units/qualifiers/ranges, time/provenance, unknowns/corrections, privacy/security, accessible error workflow, verification, and named human review.

## Answers to the Exercises

### Answer 1

Map immutable source message/order IDs to namespaced target equivalents and preserve causation/tenant. Convert `amount_minor` plus ISO currency to exact decimal amount plus currency/scale; reject unsupported currency/range and specify line-versus-total rounding. Presence table keeps missing delivery date as unknown/not-provided, explicit null as not-applicable only if source defines it, empty lines as valid/invalid per invariant, and zero/false as present.

Map every v1 status to v2 with meaning: preserve unknown raw code or reject; never default to active. Parse occurrence timestamp with offset/precision and preserve it, while translation time is separate. Preserve line order, stable line ID, duplicates, quantity/unit, and product identity; unknown source fields remain in protected provenance only if contract/privacy permits. Validate source, target totals/status/time/tenant invariants. Provenance binds source digest, v1/v2 schemas, mapping/reference versions, target ID, loss ledger, and outcome. Typed errors distinguish malformed, unsupported, semantic, unauthorized, target-invalid, and infrastructure.

Round-trip subset includes supported currencies/statuses/timestamps, representable scale/range, all required identities, and presence/line distinctions representable in v2. Independently implemented reverse mapping must recover semantic v1 values; fields intentionally removed/merged or precision reduced are excluded and listed as loss, not hidden.

### Answer 2

(a) Integer cents to text is injective if integers are unbounded/in target range, currency has exactly two minor digits under fixed policy, sign is preserved, text parser requires canonical two decimals, and no rounding occurs: reverse `major*100+minor` recovers source. It is not universally lossless for currencies/scales other than two, overflow-limited targets, or noncanonical rounded decimals.

(b) List to set is lossy: `[A,B]` and `[B,A]` differ in order but yield the same set; `[A,A]` and `[A]` differ in multiplicity but yield the same set. Only a subset with unique elements and irrelevant/canonical order can be semantically equivalent.

(c) Five to three statuses is non-injective by pigeonhole principle if all five are semantically distinct: at least two share target. It is acceptable only if source equivalence already groups them for target purpose and loss is declared.

(d) Zoned local time plus zone/offset to UTC instant loses zone identity and civil-time intent: Stockholm and another zone/offset can yield the same instant; future recurrence behavior differs. It is lossless only for semantics defined solely as an instant and with enough disambiguation to compute it. Preserve zone/provenance when schedule meaning matters.

### Answer 3

Pure translator maps source fields using an immutable country/currency table version bundled or content-addressed by mapping context. If source lacks authoritative country/currency, a separate enricher obtains it under tenant/purpose authorization, freshness/deadline/cache policy and emits explicit evidence; translator then consumes the enriched typed source. Do not hide a network call inside field mapping.

Cache is keyed by reference version, verified, bounded, and immutable; control-plane outage can continue only with an approved still-valid version, else quarantine/fail closed. Historical replay uses recorded mapping/table versions; intentional current-policy remap is a new authorized backfill with new operation identity. Deploy schema/table/mapping compatibility tests, shadow outputs/digests/loss, canary, fence unsafe mixed epochs, retain rollback and old versions through retention.

Minimize fields, authenticate/authorize source and lookup, prevent cross-tenant keys, encrypt/protect tables/provenance/quarantine, and redact telemetry. Measure version skew, lookup/enrichment freshness/failure, unknown code, rounding/loss/default, translation errors, quarantine age, output publish, and reconciliation. Reconcile source/target identity/count, currency totals per code/version, and provenance; fault-test reference outage/staleness/tampering and every ack/publish boundary.

### Answer 4

Inventory each mapping's semantic fields, versions, consumers, retained history, defects, loss, and owner; cluster integrations by coherent bounded domain. Establish canonical vocabulary through domain/data/privacy governance with identity, presence, units, time, enums, provenance, extension/evolution rules, and explicit non-goals. Do not force specialized concepts into a global lowest-common-denominator schema.

Add source-to-canonical and canonical-to-target beside one low-risk pair. Shadow both against existing direct output over historical/adversarial fixtures; compare semantic projections, identity, counts, amounts, statuses, ordering, loss, and performance. Keep direct path authoritative until reviewed parity; then cut one target to canonical path with stable IDs/dedupe, compatibility window, canary, reconciliation, and rollback routing. Never let both paths cause effects.

Migrate one edge at a time, retain source evidence and old translator/version for in-flight/replay, and add new concepts additively. If canonical loses required semantics, extend it or retain an anti-corruption direct mapping. Retire a pair only after producers/history drained, downstream effects reconciled, rollback/forward rehearsed, and monitoring proves no use. Governance metrics track mapping count/churn, unknown/default/loss, version skew, and semantic incidents rather than celebrating fewer files alone.

### Answer 5

Preserve patient/tenant/specimen/order/result/analyte identities; source and target laboratory code systems with exact version; original code/display; value as exact decimal/range/ordinal/text with comparator such as `<` or `>`; unit using governed ontology; reference range with population/method context; abnormal/critical qualifiers; status preliminary/final/corrected/cancelled; collection/observation/effective times with zone/precision; instrument/method/laboratory provenance; source result version and correction lineage. Never convert censored `>500` to exact 500, missing to normal, or unknown code to a common analyte.

Validate dimensional compatibility and conversion formula/range/rounding independently; preserve original value/unit and mapping/code-table versions. Unknown, conflicting, stale, unrepresentable, or unauthorized results enter a patient-safe, time-bounded clinical escalation—not silent default. Corrections supersede/link rather than overwrite audit. Enforce tenant/patient/purpose/professional authority, integrity, minimization, encryption, retention, redacted logs/quarantine, and controlled inspection.

Operator workflow clearly distinguishes pending, translated, unavailable, ambiguous, corrected, and overridden using keyboard/screen-reader/color-independent cues and records clinical rationale. Verify official clinical test vectors, boundaries/dimensional properties/mutation, historical/differential round trips where valid, schema/code-system compatibility, duplicates/gaps/corrections, crashes/replay, authorization/privacy attacks, parser fuzz, load, accessibility, reconciliation, and disaster recovery. Named laboratory medicine specialists, treating clinicians/pharmacists as relevant, clinical safety/informatics, patients/representatives, terminology experts, privacy/legal/regulatory, security, accessibility/human-factors, data/integration/SRE, and incident-response owners review actual mappings. Automated tests cannot establish clinical equivalence.
