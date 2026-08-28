---
module_id: SEPAT-021
program: Software Engineering: Patterns
level: 1
module_number: 21
title: Adapter
status: complete
last_verified: 2026-08-28
---

# Adapter

## One-Page Review

### Governing question

How can an existing interface, representation, or protocol satisfy a required contract without leaking foreign semantics, weakening invariants, or pretending that lossy translation is equivalence?

### Essential definitions

- An **Adapter** converts the interface of an adaptee into a target interface expected by a client.
- The **target** is the contract owned by the consuming context; the **adaptee** is the existing component being integrated.
- An **object adapter** delegates to a wrapped adaptee; a **class adapter** uses inheritance where the language and ownership allow it.
- **syntactic adaptation** changes names, parameter shapes, or call conventions while preserving meaning.
- **semantic adaptation** translates units, identities, states, errors, time, or business concepts and carries greater proof burden.
- **impedance mismatch** is a structural or semantic difference between connected models.
- An **anti-corruption layer** is a broader boundary of adapters/translators that protects one domain model from another.
- **round-trip law** tests whether converting out and back preserves a defined observation; many legitimate adapters are intentionally one-way.
- **loss budget** records information discarded, approximated, defaulted, or made unavailable.
- **contract test** checks multiple adapter implementations against target behavior, including failures and boundaries.

### Central model, mechanism, or theorem

Let legacy valid inputs be \(L_v\subseteq L\), target values \(T\), and partial adapter \(f:L\rightharpoonup T\). Correctness requires

\[
\forall x\in L_v,\quad invariant_T(f(x))
\]

and each invalid or unrepresentable \(x\) must produce a declared target error rather than silent corruption. If reverse mapping \(g:T\rightharpoonup L\) is claimed lossless over domain \(D\), require an observational round trip \(g(f(x))\equiv_D x\). Interface conformance alone is insufficient: timing, failure, ordering, cancellation, transaction, authority, and side-effect semantics must refine the target contract.

### Critical invariants

- The target contract is defined independently of the adaptee and uses target-domain vocabulary.
- Every unit, encoding, identifier, nullability, range, timestamp, and enum mapping is explicit.
- Unsupported or lossy cases are classified; no silent default creates a valid-looking wrong value.
- Error, timeout, cancellation, retry, ordering, idempotency, and partial-success semantics remain target-compatible.
- Resource ownership and thread/task affinity cross the boundary deliberately.
- Authentication context and capabilities are narrowed, validated, and never logged as secrets.
- Bidirectional adapters state round-trip laws and canonicalization exceptions.
- Adapter observability distinguishes upstream, translation, target-validation, and downstream failures.

### Common failures

Common failures include renaming methods while ignoring semantic differences, unit conversion with rounding overflow, mapping every foreign error to “unknown,” substituting local time for missing instants, treating empty and absent as equal, leaking foreign DTOs into the domain, hiding blocking calls behind an async target, retrying non-idempotent legacy operations, preserving stale credentials in adapted objects, assuming list order or pagination stability, mixing business orchestration into a universal adapter, and retaining an obsolete adapter after migration ends.

### Compact example

A target requests temperature in integer millidegrees Celsius. A legacy sensor returns tenths Fahrenheit plus a quality code. The adapter validates station identity and quality before an exact conversion for the demonstrated value; a bad-quality result becomes a target error. The target never sees the legacy dictionary or quality code.

### Connections

[SEPAT-020](020-comparing-creational-patterns-under-change.md) provides evidence-based selection. [SEPAT-022](../ROADMAP.md) separates two dimensions that evolve independently, while [SEPAT-025](../ROADMAP.md) simplifies a subsystem rather than converting one contract. Adapter connects to [Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), and [Data Engineering](../../19-data-engineering/ROADMAP.md).

## Governing Question

What exact target behavior must clients rely on, which foreign behaviors can be translated faithfully, and where must the boundary reject, expose loss, or renegotiate the contract?

Adapter is appropriate when the target contract is sound and an existing component can implement it through bounded conversion. If the target itself is vague or the semantic gap is irreconcilable, an adapter merely conceals uncertainty. Define both contracts before writing glue.

## Why This Matters

Integration defects often compile. A field named `amount` may be minor units in one system and decimal major units in another. “Success” may mean durable commit, queued acceptance, or an eventually attempted operation. An adapter that makes signatures match can transform visible incompatibility into silent corruption.

A disciplined adapter localizes foreign change, protects domain vocabulary, and creates a testable place for compatibility policy. It also documents what cannot be preserved. This is especially valuable during migrations and vendor integration, where change control and trust differ across the boundary.

## Prerequisites and Retrieval

You should understand interfaces, delegation, type conversion, invariants, errors, units, time, protocols, and contract testing. Retrieve these facts:

1. Type compatibility does not imply semantic compatibility.
2. Floating-point, integer width, rounding mode, and overflow are part of a conversion contract.
3. Missing, null, empty, zero, and unknown can represent distinct domain states.
4. A synchronous call cannot implement an asynchronous delivery guarantee merely by returning early.
5. Retry safety depends on operation semantics and idempotency keys, not transport error names.
6. Bidirectional translation can be impossible when either model has more states or information.

## Learning Objectives

After completing this module, you should be able to:

- distinguish syntactic from semantic adaptation;
- define target and adaptee contracts independently;
- specify total, partial, lossy, and bidirectional mappings;
- preserve units, identity, time, errors, ordering, and side-effect semantics;
- design adapters across sync/async, transaction, streaming, and resource boundaries;
- test refinement, boundary cases, metamorphic laws, and failure translation;
- place adapters within anti-corruption and migration boundaries;
- recognize when rejection or contract change is safer than adaptation.

## Core Exposition

### Own the target contract

The consuming domain defines names, types, invariants, errors, and effects. Do not derive its public contract by mechanically mirroring a vendor schema. The adapter depends inward on that target and outward on the adaptee.

Keep foreign DTOs, SDK exceptions, enum values, and pagination tokens at the boundary. If they spread through domain code, the adapter has not isolated change.

### Object and class adapters

Object adapters wrap an adaptee and delegate. They can adapt final/closed classes, select among instances, and expose only narrow authority. They are usually the durable default.

Class adapters inherit adaptee implementation while satisfying the target. They can override protected behavior but couple to inheritance layout and may expose more surface. Use only when substitutability and lifecycle of both hierarchies are valid.

### Inventory the semantic gap

Build a mapping table for every operation and field: target meaning, source meaning, conversion, validation, loss, error, ownership, and evidence. Include units, range, precision, encoding, locale, calendar/time zone, identifier namespace, version, enum openness, default, optionality, and cardinality.

Unknown source enum values should usually become an explicit `UnsupportedValue` carrying safe diagnostic context—not the closest known case.

### Numeric and unit conversion

Choose exact internal units when possible. Specify rounding direction and ties, overflow policy, saturation versus rejection, negative values, and sentinel values. Test minima, maxima, halfway values, and values just outside target range.

Do not use display rounding for accounting, dosage, coordinates, or protocol sequence numbers. Record source and target unit in types or field names.

### Time and identity

Distinguish instants, local civil time, durations, monotonic deadlines, and dates. A local timestamp without zone/offset may be ambiguous or nonexistent. Reject or require context; do not invent UTC.

Identifiers need namespace and lifecycle. Vendor account `42` is not globally the same as internal account `42`. Store a mapping with provenance and collision rules when identities differ.

### Errors and partial outcomes

Create a target error taxonomy that callers can act on: invalid input, unsupported mapping, unavailable, deadline, conflict, unauthorized, indeterminate outcome, and internal defect. Preserve the causal foreign code in bounded diagnostic metadata when safe.

Do not collapse “request may have committed but response was lost” into a retryable failure. The adapter must expose indeterminate outcome or use an idempotency/reconciliation protocol.

### Sync, async, and cancellation

A blocking adaptee behind an async method still consumes a thread and may ignore cancellation. Use a bounded execution bridge, propagate deadline where supported, and document whether cancellation abandons waiting or aborts the underlying operation.

An event source adapted to request/reply needs correlation, timeout, duplicate handling, and late-response policy. Returning after enqueue is not completion unless the target contract says accepted-for-processing.

### Collections, streams, and pagination

List adaptation must define order, duplicates, snapshot consistency, page boundaries, continuation token ownership, partial page failure, and backpressure. Eagerly collecting an unbounded stream violates a streaming target.

Adapt pull to push or blocking to reactive protocols only with demand and cancellation semantics. Buffer limits and overflow policy are part of correctness.

### Transactions and consistency

If a target operation claims atomicity but the adaptee exposes multiple nontransactional calls, local sequencing is not an implementation. Change the target, add compensation with explicit limitations, or use a capable transactional boundary.

Map isolation, commit, rollback, duplicate, and concurrency-conflict semantics. Never infer durability from a 2xx response without the foreign contract.

### Security boundary

Validate all foreign input as untrusted. Normalize only when canonicalization rules are defined. Prevent injection through paths, headers, queries, templates, and logs. Redact credentials and regulated data.

Translate broad SDK clients into narrow target capabilities. The adapter should not grant callers access to arbitrary vendor operations merely because one client object exposes them.

### Version evolution

Tolerate additive foreign fields where safe, reject unknown semantics that affect invariants, and version breaking mappings. Run contract tests against supported versions and representative recorded fixtures with privacy controls.

During dual-read/write migration, compare normalized observations and handle side effects carefully. Remove the adapter after its foreign boundary disappears unless it remains a deliberate domain boundary.

### Observability

Record target operation, adapter version, upstream version, outcome class, latency partitions, conversion rejection, unknown enum, overflow, retry/duplicate, and reconciliation result. Correlation identifiers must not become unbounded metric labels.

Logs should preserve enough safe source context to diagnose mapping without dumping secrets or complete payloads. Measure adapter latency and failure separately from adaptee latency and failure.

## Definitions and Notation

Let \(C_T\) be target contract, \(C_L\) legacy/adaptee contract, \(L_v\) source states accepted by policy, and partial mapping \(f:L\rightharpoonup T\). Target refinement requires valid mapped output and compatible observable behavior:

\[
x\in L_v\Rightarrow invariant_T(f(x)),\qquad trace(adapter(x))\preceq C_T.
\]

The trace relation covers results, errors, side effects, ordering, and timing guarantees declared by \(C_T\). Let loss function \(\ell(x)\) enumerate information not represented in \(f(x)\). A claimed lossless bidirectional adapter with reverse \(g\) requires defined observational laws such as \(g(f(x))\equiv x\) over a stated domain, not byte equality after canonicalization.

## Mechanisms, Invariants, or Proof Structure

### Mapping proof obligations

For each constructor/operation, prove or test: source precondition maps from a valid target request; source success maps to a target-valid result; each source failure maps to a declared target outcome; side effects satisfy target ordering/idempotency; and rejected source states cannot escape as target values.

### Refinement limits

If the target promises a stronger property than the adaptee can provide—atomic commit, tighter deadline, total ordering, or exact precision—no structural wrapper can create it without an additional mechanism. The correct result is infeasibility, contract weakening, or a new coordinating component.

### Metamorphic and round-trip testing

Use exact fixtures for boundaries, property tests for invariants, metamorphic relations for equivalent transformations, differential tests against trusted implementations, and round trips only where reversibility is claimed. Fuzz malformed payloads and unknown future fields.

### Executable temperature adapter

<!-- bijux-verify: {"id":"validated-temperature-adapter","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"station=north\ncelsius=25.000\nlegacy-calls=1\nbad-quality-rejected=True\n","stderr":""}} -->
```python
class TemperatureReading:
    def __init__(self, station, celsius_milli, observed_epoch):
        if not (-100000 <= celsius_milli <= 100000):
            raise ValueError("temperature outside target range")
        self.station = station
        self.celsius_milli = celsius_milli
        self.observed_epoch = observed_epoch


class LegacySensor:
    def __init__(self, records):
        self.records = records
        self.calls = 0

    def read_raw(self, station):
        self.calls += 1
        return self.records[station]


class LegacyTemperatureAdapter:
    def __init__(self, sensor):
        self.sensor = sensor

    def read(self, station):
        raw = self.sensor.read_raw(station)
        if raw["station_code"] != station:
            raise ValueError("station identity mismatch")
        if raw["quality"] != "OK":
            raise ValueError("unusable sensor quality")
        numerator = (raw["fahrenheit_tenths"] - 320) * 5000
        if numerator % 90 != 0:
            raise ValueError("conversion requires declared rounding")
        return TemperatureReading(station, numerator // 90, raw["observed_epoch"])


sensor = LegacySensor({
    "north": {
        "station_code": "north",
        "fahrenheit_tenths": 770,
        "quality": "OK",
        "observed_epoch": 1787875200,
    },
    "south": {
        "station_code": "south",
        "fahrenheit_tenths": 680,
        "quality": "BAD",
        "observed_epoch": 1787875200,
    },
})
adapter = LegacyTemperatureAdapter(sensor)
reading = adapter.read("north")

try:
    adapter.read("south")
    rejected = False
except ValueError:
    rejected = True

print(f"station={reading.station}")
print(f"celsius={reading.celsius_milli / 1000:.3f}")
print(f"legacy-calls={sensor.calls - 1}")
print(f"bad-quality-rejected={rejected}")
```

The run proves the exact 77°F-to-25°C conversion for one integer input, validates identity and quality for two finite records, and prevents a bad-quality target value. It does not establish rounding for other temperatures, physical sensor accuracy, concurrent access, network behavior, timestamp validity, or safety suitability.

## Alternatives and Trade-Offs

**Direct dependency on the foreign interface** is simplest when semantics already match and foreign coupling is acceptable. Do not add an adapter that only renames without a change boundary.

**Facade** offers a simpler subsystem entry point but need not make an adaptee satisfy an existing target interface. It may use several adapters internally.

**Bridge** separates two abstractions designed to vary independently; Adapter typically reconciles an existing mismatch after interfaces exist.

**Decorator** preserves the same contract while adding responsibility; Adapter changes the contract. A wrapper can play both roles, but document each responsibility.

**Proxy** preserves a target interface while controlling access, location, or lifecycle. Translation beyond access semantics makes it partly an adapter.

**Anti-corruption layer** is appropriate when translation spans many types, operations, and domain concepts. Keep it cohesive; avoid one universal mapper bucket.

**Change either side** is best when both are owned and the mismatch has no enduring value. An adapter should not fossilize a typo or poor contract unnecessarily.

## Failure Modes and Misconceptions

- **“It compiles, so it adapts.”** Semantic and operational refinement remain unproven.
- **“Adapters are trivial glue.”** Boundary code carries units, identity, authority, and failure risk.
- **“Every error maps to one exception.”** Callers lose retry, reconciliation, and authorization decisions.
- **“Defaults preserve compatibility.”** A valid-looking invented value can be worse than rejection.
- **“Round trip must equal bytes.”** Canonicalization may change representation while preserving defined observation.
- **“Async wrappers make blocking calls nonblocking.”** They may only move blocking to a worker pool.
- **“Retries belong in every adapter.”** Retry policy depends on idempotency, deadlines, and system-level amplification.
- **“One generic mapper reduces duplication.”** It often erases domain vocabulary and concentrates unrelated change.
- **“Foreign identifiers are globally unique.”** Namespace and lifecycle must be mapped.
- **“Migration adapters are permanent.”** Define retirement evidence and remove obsolete boundaries.

## Worked Examples

### Example 1

A payment vendor reports decimal major currency units while the domain uses integer minor units and currency-specific scale. The adapter rejects unsupported currencies and nonrepresentable fractions rather than rounding silently. **Conclusion:** Money conversion is semantic validation, not field copying.

### Example 2

An `InputStreamReader` converts byte streams to character streams using a specified charset and stateful decoder. Malformed input policy and buffering affect results. **Conclusion:** Even canonical adapters need encoding and error contracts.

### Example 3

A blocking vendor SDK is exposed through an async target using a bounded worker pool. Caller cancellation detaches waiting but cannot abort the SDK call; saturation returns a declared unavailable result. **Conclusion:** Scheduling limitations must remain visible.

### Example 4

A legacy order status `DONE` means packed, while the new domain's `Completed` means delivered. The mapping is rejected; new target states `Packed` and `Delivered` preserve semantics. **Conclusion:** Similar labels are not equivalent states.

### Example 5

A paginated API gives unstable pages during concurrent writes. The target cannot promise snapshot iteration, so it exposes best-effort pages with duplicate handling instead. **Conclusion:** An adapter cannot synthesize consistency without support.

### Example 6

An event adapter maps at-least-once messages into domain commands using source event ID as an idempotency key and records poison mapping failures separately. **Conclusion:** Delivery and duplication semantics are part of adaptation.

### Example 7

Local timestamps from a legacy scheduling system omit zone. The adapter requires site metadata and rejects ambiguous daylight-saving overlaps unless a disambiguation flag exists. **Conclusion:** Inventing an instant corrupts time semantics.

### Example 8

A vendor client exposes account reads, transfers, credential rotation, and administration. The adapter implements only `ReadBalance` for a reporting context. **Conclusion:** Interface adaptation can reduce authority.

### Example 9

During migration, old and new customer models exchange data through an anti-corruption layer. Normalized differential observations are monitored until all old callers leave, then the adapter is deleted. **Conclusion:** Migration boundaries need retirement criteria.

### Example 10

An aircraft sensor adapter proposes converting vendor quality flags into a boolean `valid`. Unknown and degraded states would be lost. The target adopts a richer quality model and requires named avionics review and hardware evidence. **Conclusion:** High-stakes loss must be explicit or adaptation is infeasible.

## Cross-Program Connections

- **Domain Modeling:** bounded contexts and anti-corruption layers protect vocabulary and invariants.
- **Programming Languages:** traits, protocols, conversions, ownership, and sum types express adapter contracts.
- **API Engineering:** versioning, pagination, idempotency, errors, and compatibility dominate service adapters.
- **Data Engineering:** schema evolution, identifiers, nullability, units, and provenance govern mappings.
- **Concurrent Programming:** blocking bridges, cancellation, ordering, backpressure, and thread affinity affect behavior.
- **Distributed Systems:** retries, duplicates, partial outcomes, clocks, and consistency limit refinement.
- **Security Engineering:** validation, canonicalization, credentials, injection, and least authority meet at boundaries.
- **Testing and Quality:** contract, property, fuzz, differential, and metamorphic tests provide complementary evidence.
- **Reliability Engineering:** timeouts, saturation, observability, reconciliation, and dependency failure shape operations.
- **Systems Engineering:** physical units, calibration, timing, and safety classification constrain translation.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Adapter intent, object/class structures, participants, and consequences.
2. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003, ISBN 978-0-321-12521-7. Defines bounded contexts and Anti-Corruption Layer for semantic isolation.
3. Microsoft, [“Anti-Corruption Layer pattern”](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer), Azure Architecture Center, accessed 2026-08-28. Discusses subsystem translation, trust validation, latency, consistency, observability, operations, and retirement.
4. The Rust Project Developers, [`std::convert::TryFrom`](https://doc.rust-lang.org/std/convert/trait.TryFrom.html), accessed 2026-08-28. Specifies controlled fallible conversions and distinguishes them from perfect `From` conversions.
5. Oracle, [`java.io.InputStreamReader`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/io/InputStreamReader.html), Java SE 25 API, accessed 2026-08-28. Documents byte-to-character adaptation through a named or configured charset decoder.
6. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, ISBN 978-1-4493-7332-0. Provides encoding evolution, time, distributed failure, consistency, and stream-processing context.
7. Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall, 2004, ISBN 978-0-13-117705-5. Provides seams and incremental characterization strategies for safely isolating legacy dependencies.

## Exercises

### Exercise 1

Formalize the executable temperature adapter, recompute its conversion, identify every implicit assumption, and design exact rounding policy for inputs that do not map to integer millidegrees Celsius.

### Exercise 2

Design an adapter from a blocking, at-least-once legacy payment API to an async target that exposes deadlines, idempotency, authorization, and indeterminate outcomes. State what cannot be faithfully adapted.

### Exercise 3

Specify a bidirectional adapter between two customer schemas with different identifier namespaces, address structures, nullability, enum openness, and timestamp precision. Define loss and round-trip laws.

### Exercise 4

Plan an incremental anti-corruption layer for replacing a legacy inventory subsystem. Include ownership, contract testing, dual-operation evidence, observability, rollback, and deletion criteria.

### Exercise 5

An unfamiliar intensive-care device emits physiological values, quality flags, local timestamps, and sequence numbers through a vendor protocol. Produce a graduate-level adapter and evidence review without claiming clinical safety.

## Answers to the Exercises

### Answer 1

The accepted source set contains records whose requested and returned station codes match, quality is exactly `OK`, required fields exist with correct types, timestamp meets target policy, and converted temperature is within target range. For Fahrenheit tenths \(F_{10}\), Celsius millidegrees are \((F_{10}-320)5000/90\). At 770, numerator is \(450\times5000=2{,}250{,}000\); division by 90 gives 25,000 exactly.

Implicit assumptions include trustworthy dictionary types, station key presence, known quality vocabulary, integer width, epoch unit and time scale, physical calibration, Fahrenheit definition, target range, and one read being representative. For nonintegral results, define rational conversion first, then an explicit rounding mode such as nearest millidegree with ties-to-even and checked range; retain source value/unit for audit if allowed. Test values around zero, negatives, halfway cases, extrema, overflow, unknown quality, missing fields, mismatched identity, and invalid timestamps. Safety or sensor-accuracy claims require external calibration evidence.

### Answer 2

Expose `authorize_and_submit(command, idempotency_key, deadline) -> accepted|declined|indeterminate|unavailable`. Validate amount/currency/account and authorization before entering the adapter. Persist or deterministically bind the target idempotency key to the legacy request identity. Run blocking calls in a bounded bulkhead; deadline expiry detaches the caller but does not claim the foreign operation stopped. Correlate late results and provide reconciliation/query by idempotency key.

Map definitive business decline separately from authentication failure, capacity/unavailability, invalid request, and response-lost-after-possible-commit. Retry only when the foreign contract proves nonacceptance or honors the same idempotency key. A legacy API without idempotency/query cannot be faithfully adapted to exactly-once or definitive timeout semantics; expose indeterminate outcome, add durable orchestration/reconciliation, or reject the target promise. Measure queue and foreign latency, saturation, duplicates, late completion, and reconciliation. Never log credentials or full payment data.

### Answer 3

Create explicit source and target DTOs at the boundary and a durable identity map keyed by `(source_system, source_id, lifecycle_generation)`. Address conversion preserves structured components and provenance; a free-form source address cannot losslessly become verified structured fields, so mark unverified/original text or reject based on use. Keep absent, explicit null, empty, and redacted distinct when either model distinguishes them. Map known enums and preserve an `Unknown(source_code)` case rather than choosing a known value. Timestamp conversion records source precision; do not invent subsecond accuracy.

Define loss record \(\ell(x)\) listing discarded order, unrepresentable components, precision reduction, canonicalization, and unknown fields. On the common lossless subset \(D\), require `to_source(to_target(x))` observationally equals `x` for identity, normalized address, semantic enum, null state, and timestamp at source precision. Outside \(D\), return a typed lossy result requiring caller acceptance or reject. Property-test laws, collisions, Unicode/canonical forms, future enums, precision boundaries, and identity reuse.

### Answer 4

Define the new inventory target contract independently: item identity, reservation, release, availability, error, concurrency, and consistency semantics. Place adapters in one owned boundary package/service, not scattered call sites. Characterize legacy behavior and build contract tests plus fixtures. Migrate one vertical capability at a time through the boundary; prohibit new direct legacy imports.

For reads, shadow the new implementation and compare normalized observations with explained consistency windows. For writes, avoid naive dual writes; use an owned durable outbox/change-capture or reconciliation design with idempotency and explicit authority. Version identity mappings and translation rules. Observe call counts, translation failures, unknown values, latency, divergence, duplicates, reconciliation age, and direct-access violations. Rollback routes through a versioned switch while preserving the authoritative source and pending work. Delete adapters after all consumers migrate, direct-access checks are zero, reconciliation backlog is zero, retention/audit obligations pass, and an agreed observation window succeeds; remove legacy credentials and infrastructure too.

### Answer 5

First define target types with physical quantity and unit, device/channel identity, monotonic sequence, authenticated observation instant, receive instant, and a rich quality sum type that preserves known/degraded/invalid/unknown states. Reject unknown critical semantics; never collapse them to valid. Resolve local time only with device/site zone, clock status, offset, ambiguity flag, and synchronization evidence. Detect duplicate, gap, regression, wrap, reboot generation, stale age, and out-of-range values. Preserve raw signed frames in controlled audit storage where policy permits.

The adapter validates framing, authentication/integrity, schema/version, device binding, unit/range, calibration version, quality, sequence, and time before creating a domain observation. It exposes missing/invalid/indeterminate explicitly, applies no clinical alarm or diagnosis policy, and uses bounded buffers/backpressure with fail-safe handling. Threat-model malformed frames, replay, spoofing, downgrade, key rotation, resource exhaustion, log injection, and privacy leakage.

Evidence includes protocol conformance, independent unit/numerical recomputation, calibration traceability, property/fuzz testing, corrupted/truncated/reordered/duplicate/replayed frame injection, clock drift/reset/wrap tests, timing and buffer analysis, hardware-in-the-loop, cybersecurity assessment, end-to-end alarm-path validation, and controlled clinical workflow evaluation. Named clinical specialists for each measured quantity, biomedical engineers, device/vendor experts, real-time and embedded engineers, functional-safety, cybersecurity, human-factors, quality, regulatory, operations, and independent verification reviewers must approve. This chapter and toy conversion establish no clinical accuracy, alarm safety, or deployment suitability.
