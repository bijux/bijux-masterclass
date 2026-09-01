---
module_id: API-030
program: API & Service Engineering
level: 1
module_number: 30
title: Reviewing a Contract for Ambiguity and Incompleteness
status: complete
last_verified: 2026-09-01
---

# Reviewing a Contract for Ambiguity and Incompleteness

## One-Page Review

### Governing question

How can reviewers find places where an API contract permits incompatible interpretations or omits a decision that consumers need, then turn each finding into precise, testable, owned language?

### Essential definitions

- **ambiguity** exists when competent readers can derive multiple materially different meanings from the same contract.
- **incompleteness** exists when a consumer-relevant situation has no specified outcome or decision rule.
- An **interpretation** maps a contract statement and context to permitted observable behavior.
- A **decision table** enumerates relevant conditions and required outcomes.
- A **witness** is a concrete request, state, actor, or execution that exposes competing interpretations or a missing case.
- A **normative statement** says what conforming parties are required, prohibited, recommended, or permitted to do.
- **traceability** links consumer task, requirement, contract element, example, implementation evidence, and owner.

### Central model, mechanism, or theorem

For contract $C$ and situation $x$, let $I(C,x)$ be the set of reasonable consumer-visible interpretations. Ambiguity exists when $|I(C,x)|>1$; incompleteness exists when no supported outcome is defined for a required situation. Review seeks a refined contract $C'$ such that each in-scope situation has one bounded outcome set, with any intentional freedom stated explicitly. Completeness is always relative to scope and risk; finite review cannot prove every future situation covered.

### Critical invariants

Every operation has an actor, preconditions, success meaning, failures, observable effects, and lifecycle. Terms have one definition and units. Required, optional, absent, null, empty, default, and unknown are distinct. Request accepted sets and response produced sets are explicit. Status, headers, media type, body, and state transition agree. Authorization includes disclosure policy. Pagination, ordering, concurrency, retries, idempotency, time, limits, and asynchronous completion are decided where relevant. Examples witness rules but do not replace them. Each finding has owner, severity, resolution, and evidence.

### Common failures

Reviewing only schema syntax; asking whether prose “looks clear”; using “normally,” “as needed,” “valid,” “soon,” or “latest” without a rule; undocumented defaults; optional fields with required semantics; broad `default` errors; happy-path-only responses; overlapping unions; missing units and time zones; unspecified ordering; silent truncation; confused absence and null; authorization described only as authentication; retries without effect identity; generated clients treated as interpretation proof; and closing a finding by adding one example while leaving the rule ambiguous.

### Compact example

The contract says `GET /orders` returns “recent orders” and accepts optional `limit`. One client assumes newest-first and default 20; another assumes unspecified order and all items. Review writes a witness with 25 orders, then specifies newest-created descending with ID tie-break, default 20, range 1–100, stable cursor semantics, and invalid-limit response. **Conclusion:** ambiguity is removed by a decision rule, boundary outcomes, and testable witnesses—not more adjectives.

### Connections

[API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md) defines promise categories. [Validation Constraints](025-validation-constraints.md) supplies accepted-set boundaries. [Examples and Executable Documentation](027-examples-and-executable-documentation.md) supplies witnesses, while [Mocking and Consumer Exploration](029-mocking-and-consumer-exploration.md) finds interpretive disagreements. [Transport, Application, and Domain Boundaries](../ROADMAP.md) next assigns implementation responsibility.

## Governing Question

Which review passes, adversarial witnesses, decision structures, and closure criteria expose ambiguous or missing API behavior before independent implementations and consumers institutionalize incompatible assumptions?

## Why This Matters

A syntactically valid OpenAPI document can still leave the most important questions unanswered. It may declare a string but not its normalization, a list but not its order, a `409` but not its cause or recovery, an optional field but not whether omission invokes a default, or a security scheme but not which actor may see a particular object. Tools can parse such a contract while consumers disagree about it.

Ambiguity is expensive because each team fills gaps locally. A server chooses one default, a generated client another, a mock a third, and documentation implies a fourth. Once released, accidental interpretations become compatibility constraints. Incompleteness is equally dangerous: a missing timeout, retry, authorization, or pagination rule may surface only under production failure.

Review is therefore a search for competing executable interpretations. Reviewers construct concrete witnesses, trace all observable parts of the exchange, and ask whether two conforming implementations could behave differently in a way that matters. Intentional variation is allowed, but it must be bounded and communicated. The goal is not maximal prose; it is the smallest complete decision structure for the promised scope.

## Prerequisites and Retrieval

Retrieve consumer tasks, HTTP semantics, OpenAPI operations and schemas, JSON Schema dialect, parameter serialization, content negotiation, status and Problem Details conventions, validation constraints, examples, compatibility, authorization, idempotency, conditional requests, pagination, asynchronous operations, contract-first/code-first authority, mocking, and evidence records.

Before review, retrieve the authoritative artifact and digest, target consumers, supported environments, prior released contract, domain vocabulary, policy sources, known incidents, usage evidence, generated-client mappings, and owners who can decide unresolved semantics.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish ambiguity, incompleteness, inconsistency, and intentional freedom;
2. review accepted inputs, produced outputs, state transitions, and operational behavior;
3. construct boundary and adversarial witnesses for competing interpretations;
4. use definitions, normative language, decision tables, state models, and examples correctly;
5. prioritize findings by consumer consequence and irreversibility;
6. close findings with authority changes and verification evidence; and
7. explain the limits of completeness claims.

## Core Exposition

### Review meanings, not document appearance

Begin with a consumer task and trace its whole observable exchange. For each operation ask:

1. Who is the actor, and what capability and tenant context apply?
2. What resource or operation is identified?
3. Which request forms are accepted, rejected, or normalized?
4. What does each success status mean and what effect occurred?
5. Which failures can the consumer distinguish, and how does it recover?
6. Which headers, representations, links, and later observations matter?
7. What happens under concurrency, retry, partial failure, and time?

This task-first pass finds gaps a field-by-field review misses. A schema can describe `quantity` precisely while the task remains impossible because the consumer lacks a product version or price identity.

Then perform artifact passes: structure and references; vocabulary and units; accepted input set; produced output set; HTTP coherence; state and temporal behavior; security and privacy; operational limits; compatibility; and evidence. Separate the passes so a polished description does not distract from missing failure semantics.

### Classify the defect accurately

Four classes require different repairs:

- **ambiguity:** one statement supports multiple material meanings;
- **incompleteness:** a relevant case lacks a statement;
- **inconsistency:** two statements prescribe incompatible outcomes; and
- **intentional freedom:** several outcomes are deliberately permitted within a stated bound.

“Results are ordered by date” is ambiguous if creation and modification dates exist, direction is absent, and ties are unspecified. No rule for an expired cursor is incomplete. Saying both “cursor never expires” and “cursor lifetime is 24 hours” is inconsistent. Saying a server may return `200` or `202` based on whether completion is immediate can be intentional freedom only if both meanings and consumer handling are defined.

Do not label uncertainty “implementation-defined” casually. That phrase shifts interoperability cost to every consumer. Preserve freedom only where it creates real value and consumers can handle all permitted outcomes.

### Build an interpretation set

For statement $c$ and context $x$, enumerate credible interpretations:

$$
I(c,x)=\{i_1,i_2,\ldots,i_n\}.
$$

The review question is not whether the author knows what was intended. It is whether an independent implementer can derive the same bounded behavior from the published sources. Write each interpretation as an observable outcome.

For “blank names are ignored,” possible interpretations include removing surrounding whitespace, treating empty string as absent, silently dropping an array element, accepting a record without a name, or rejecting the request. A concrete payload containing missing, null, empty, whitespace-only, and ordinary names separates them.

Intentional alternatives remain in $I$, but the contract names them and states how consumers distinguish or tolerate them. Undocumented alternatives are defects.

### Define terms and normative strength

Create one domain vocabulary for words such as account, customer, member, principal, order, reservation, cancellation, active, available, and settled. Avoid synonyms unless they represent different concepts. Link identifiers to the entity and lifecycle they identify.

Use ordinary direct requirements language. When BCP 14 terms such as `MUST`, `SHOULD`, and `MAY` are adopted, cite RFC 2119 and RFC 8174 and use them consistently. `SHOULD` is not a softer substitute for indecision: a valid exception must be understood, and interoperability consequences matter. Product contracts often work better with “The service returns…” and explicit alternatives than dense pseudo-standard language.

Replace vague qualifiers:

- “soon” with a contractual bound or explicitly non-contractual expectation;
- “large” with a measured limit and unit;
- “valid” with named validation predicates;
- “latest” with timestamp field, ordering direction, tie-break, and consistency rule;
- “may fail” with conditions, outcome class, and recovery; and
- “where possible” with decision ownership and observable fallback.

### Audit presence, null, empty, and default

For every field, distinguish:

- absent property or parameter;
- explicit JSON `null` or protocol equivalent;
- empty string, array, or object;
- supplied valid value;
- supplied invalid value; and
- unknown property or parameter.

Optional presence does not define the semantics of omission. Does the receiver choose a default, preserve an existing value, clear it, infer it, or reject a cross-field combination? JSON Schema `default` is an annotation and does not generally insert a value. If the server applies a default, state the behavior and show it in response or observation where relevant.

For updates, the distinctions are crucial. In a merge-like patch, omission might mean unchanged while null means clear. In a replacement, omission might remove or default. Define per operation rather than relying on one schema name.

Close object and union behavior intentionally. If unknown request properties are rejected, state and validate it. If unknown response properties may appear, consumer compatibility guidance must permit tolerant reading. For `oneOf` or `anyOf`, construct witnesses that match zero, one, and multiple branches.

### Audit numbers, strings, and units

A numeric bound without a number model can remain ambiguous. Define integer versus decimal, exactness, precision, scale, rounding mode, overflow, and serialization. Money needs currency ownership and minor-unit or decimal semantics. Percentages need range and whether `0.15` means 15%.

Every measured value needs unit. Duration `30` might mean milliseconds or seconds. Size might mean bytes or characters. Timestamp contracts need format, offset requirements, precision, leap-second policy if material, and comparison semantics. Do not imply that timestamp order uniquely orders events; add a stable tie-break.

Strings need Unicode and normalization decisions only where material. Specify case sensitivity, trimming, empty behavior, allowed repertoire, and length measure. A schema regex alone may be unreadable or behave differently across engines. Explain domain meaning and test boundary characters.

### Audit collections, ordering, and pagination

For every collection ask: can it be empty, are duplicates meaningful, is order promised, what is the maximum size, and can results change during traversal? If ordered, name sort key, direction, null placement, locale/collation where relevant, and total tie-break.

Pagination needs default and maximum page size, cursor opacity, traversal direction, expiration, filter/sort binding, consistency model, duplicate and omission expectations under concurrent changes, terminal indication, invalid-cursor outcome, and whether totals are exact, approximate, or absent.

“Returns up to 100 items” does not say why fewer appear. It could mean terminal page, authorization filtering, service truncation, or transient limit. Supply a next link or cursor rule and do not let absence of data disclose hidden resources.

### Audit HTTP coherence

Review method properties, selected representation, status, headers, and body as one claim. A `201` should identify the created resource when the API model provides one. A `204` has no content. A `304` follows conditional request semantics. A `202` needs an observation path if clients must learn completion. `Location`, validators, retry hints, caching fields, and content negotiation often carry meaning omitted from body schemas.

Document known failure statuses and stable public classification. A broad `default` response can describe an envelope but does not tell consumers which conditions are retryable, correctable, concealed, or permanent. Problem type should have stable semantics independent of localized detail.

Check intermediaries. Gateways may reject size, media type, authentication, or rate limits before application code. Decide whether those responses follow the public error contract and which component owns them.

### Audit state and time

Represent lifecycle explicitly. Let state machine be $(S,Q,\delta)$, where $S$ is public state, $Q$ relevant operations, and partial transition function $\delta:S\times Q\rightharpoonup S$. For every state-operation pair, specify transition, idempotent no-op, conflict, not found, forbidden, or intentionally unavailable behavior.

Ask when effects become observable, from which reads, under which consistency expectation, and for how long identifiers or operation resources remain usable. Separate acceptance from completion. Avoid “eventually” without a consumer observation and escalation rule; if no upper bound is promised, say so and define polling or notification behavior.

Time-based rules need clock authority and boundary inclusion. “Expires after 24 hours” leaves ambiguity at the exact instant, under skew, and relative to which timestamp. Write comparison such as `now >= expiresAt` under server clock, expose `expiresAt`, and state permitted client behavior.

### Audit concurrency, retry, and identity

Every mutating operation should answer what happens when state changes between read and write. Define validators, versions, conditional headers, conflicts, merge policy, or deliberate last-write behavior. “Latest update wins” still needs ordering authority and failure handling.

For retries, distinguish request transport identity, operation identity, resource identity, and effect identity. State which operations are safe or idempotent under HTTP semantics and which application commands require an idempotency key. Define key scope, payload mismatch, retention, replay response, concurrent duplicate handling, and failure after the effect but before response.

Without these rules, two provider implementations can both satisfy schemas while creating different numbers of effects. Include lost-response and concurrent-duplicate witnesses.

### Audit authorization and disclosure

A security scheme describes credential transport, not complete authorization. For each operation and resource relationship, define required capability, ownership or tenant rule, field-level projection, and whether inaccessible resources are concealed as not found.

Review differences among unauthenticated, expired, insufficient-scope, wrong-tenant, forbidden-field, absent-resource, and rate-limited cases. Public distinctions can leak existence or policy. Make disclosure deliberate and ensure errors, timing, caches, pagination totals, and links do not contradict it.

Ask what the consumer may infer from every field. A response schema might permit `ownerEmail`, but authorization determines whether this actor receives it. Examples should include least-privileged projections and non-disclosure cases.

### Use decision tables and witnesses

Prose becomes fragile when several conditions interact. A decision table makes coverage visible:

| Exists | Visible | Version current | Outcome |
|---|---|---|---|
| no | n/a | n/a | concealed `404` |
| yes | no | n/a | concealed `404` |
| yes | yes | no | `412` with refresh guidance |
| yes | yes | yes | update and new validator |

Verify that rows are mutually exclusive and collectively cover the promised condition space. If a combination is impossible, state the invariant that excludes it. Translate each row into a positive or negative witness.

The executable audit below checks a small decision table for missing and overlapping Boolean cases. It does not review HTTP or authorization semantics.

<!-- bijux-verify: {"id":"decision-table-coverage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"situations=8\ncovered=8\nmissing=[]\noverlapping=[]\ncoverage=complete_for_declared_boolean_space\n","stderr":""}} -->
```python
from itertools import product

situations = set(product((False, True), repeat=3))
rows = {
    "absent": {x for x in situations if not x[0]},
    "concealed": {x for x in situations if x[0] and not x[1]},
    "stale": {x for x in situations if x[0] and x[1] and not x[2]},
    "update": {x for x in situations if x[0] and x[1] and x[2]},
}
covered = set().union(*rows.values())
overlapping = sorted(
    x for x in situations if sum(x in values for values in rows.values()) > 1
)
print(f"situations={len(situations)}")
print(f"covered={len(covered)}")
print(f"missing={sorted(situations - covered)}")
print(f"overlapping={overlapping}")
print("coverage=complete_for_declared_boolean_space")
```

The final line is deliberately scoped. The table may omit actor types, deletion states, malformed validators, or races. Exhaustive enumeration over a simplified model does not prove the model complete.

### Review examples as adversarial probes

Examples should witness rules at boundaries: omitted, null, empty, minimum, maximum, just outside, unknown, stale, concurrent, unauthorized, retry, and terminal state. Ask whether each example is required by the rule or merely one permitted value.

Run examples through independent implementations or serializers where feasible. If two tools produce different wire forms or branch choices, inspect whether the contract relies on implementation-defined or undefined behavior. OpenAPI 3.2 explicitly identifies such behavior in some constructs; authors should avoid it when interoperability matters.

Do not close ambiguity by publishing two conflicting examples. Repair the rule, validate both examples, and state whether each is accepted or rejected and why.

### Separate automated and semantic review

Automation should detect unresolved references, duplicate operation identifiers, schema errors, missing responses, invalid examples, overlapping known constraints, inconsistent manifests, broken links, unannotated code, legacy math delimiters, and compatibility diffs.

Human review remains necessary for domain meaning, consumer feasibility, authorization disclosure, recovery, operational truth, and whether the modeled condition space is adequate. A linter can require descriptions but cannot ensure they make a useful decision.

Use two independent perspectives: a consumer/professor review for definitions, derivations, and learnability; and a practitioner review for implementation, intermediaries, failure, concurrency, security, and operation. Record limitations and do not claim external review without named evidence.

### Prioritize findings

Score findings by likelihood of divergent interpretation, consumer impact, security or financial consequence, number of affected consumers, irreversibility after release, and cost of later migration. A missing tie-break may be low consequence for a dashboard but high consequence for financial export pagination.

Block release for defects that can cause unsafe action, data disclosure, incompatible wire behavior, duplicate effects, unrecoverable consumer state, or an unimplementable promise. Minor wording can be scheduled only when the current behavior remains uniquely and safely derivable.

Avoid raw finding counts as quality metrics. Ten spelling findings are not equivalent to one ambiguous authorization rule. Track open decision risk, ownership, age, and evidence.

### Close a finding completely

A finding is closed only when:

1. the authoritative source changes or the existing rule is demonstrated;
2. terminology and related operations remain consistent;
3. examples and decision tables witness the resolution;
4. compatibility impact is classified;
5. generated projections are refreshed;
6. provider and consumer evidence is added where applicable; and
7. the reviewer verifies the original competing interpretations no longer survive.

“Author explained it in the meeting” is not closure. Neither is changing a mock alone. Record decision, rationale, owner, artifact digest, affected consumers, and any intentional freedom.

### State completeness honestly

Completeness is relative to declared scope $X$, model $M$, and evidence $E$. A review can establish that every row in a chosen decision table has an outcome and every declared operation passes the checklist. It cannot prove that no future consumer situation exists.

Report: “No unresolved findings in the reviewed operations and scenario set as of the stated artifact digest,” not “the API is unambiguous and complete.” Expand review when incidents, consumer feedback, tool disagreement, or one defect suggests a wider class.

## Definitions and Notation

Let $C$ be a contract, $X$ an in-scope set of situations, and $I(C,x)$ reasonable consumer-visible interpretations for $x\in X$. An ambiguity witness satisfies $|I(C,x)|>1$. An incompleteness witness identifies $x$ for which the contract gives no supported outcome or decision rule.

Let accepted request set be $A_q$ and produced response set for context $c$ be $P_r(c)$. Review checks boundaries of both sets; narrowing $A_q$ and widening $P_r$ are often consumer-risky directions.

A decision table consists of condition space $X_M$ from model $M$ and rows $R_1,\ldots,R_n$. Declared-model coverage requires:

$$
\bigcup_{i=1}^{n}R_i=X_M,
$$

and determinism requires $R_i\cap R_j=\varnothing$ for $i\ne j$, unless priority is an explicit part of the rule.

A **closure criterion** is evidence required before resolving a finding. A **tie-break** provides total ordering when the primary key is equal. A **condition-space model** names variables considered in a decision table. A **scope limitation** names variables or behaviors intentionally not established by the evidence.

## Mechanisms, Invariants, or Proof Structure

1. Pin authority, version, consumer scope, and prior contract.
2. Trace complete consumer tasks before field-level inspection.
3. Classify ambiguity, incompleteness, inconsistency, or intentional freedom.
4. Enumerate competing interpretations as observable outcomes.
5. Audit vocabulary, presence, units, collections, HTTP, state, time, retry, and authorization.
6. Build boundary witnesses, state models, and decision tables.
7. Run deterministic lint, example, compatibility, code, and math checks.
8. Perform independent conceptual and practitioner reviews.
9. Prioritize by consequence and cost of later divergence.
10. Close through authority, projections, evidence, and re-review; report scope limits.

The proof obligation for one resolved finding is local: under the stated model and scope, the revised contract removes the witnessed competing interpretations or supplies the missing decision. It is not a proof that the entire API is complete.

## Alternatives and Trade-Offs

Checklists provide repeatability and broad coverage but encourage mechanical completion. Task traces expose cross-field and temporal gaps but sample consumer journeys. Use both.

Prose expresses domain and temporal meaning well but can hide cases. Schemas precisely define many instance sets but cannot express every behavior. Decision tables expose combinations but grow exponentially. State machines clarify lifecycle but may omit data conditions. Select the smallest combination that makes decisions testable.

Strictly specifying every detail reduces consumer uncertainty but can freeze irrelevant implementation choices. Leaving freedom supports evolution but transfers complexity to consumers. Specify observable behavior required for safe independent use; leave internal mechanisms and explicitly tolerable variation open.

One centralized review board improves consistency but can become a bottleneck and lack domain context. Team-only review is fast but may miss cross-consumer effects. Use domain owners for meaning, API specialists for protocol, security reviewers for disclosure, and actual consumers for usability, with clear decision authority.

Examples make rules concrete but can be mistaken for exhaustive behavior. Property-based or generated witnesses explore more boundaries but may lack semantic meaning. Pair reviewed examples with systematic generation and label both.

Requiring zero findings before any implementation reduces early drift but delays learning. Thin contract slices with mock exploration and incremental review preserve early feedback while keeping each released slice complete enough for its task.

## Failure Modes and Misconceptions

- **“The schema validates, so the contract is clear.”** Schemas omit many HTTP, state, policy, and operational decisions.
- **“The author can explain the intent.”** Consumers need durable published meaning, not private knowledge.
- **“Optional means may be omitted with no effect.”** Omission can default, preserve, clear, infer, or conflict.
- **“Default inserts a value.”** JSON Schema `default` is annotation unless application policy says otherwise.
- **“One success response is complete.”** Known validation, state, authorization, concurrency, and operational failures matter.
- **“`default` error covers all failures.”** It may cover shape while leaving classification and recovery absent.
- **“Latest is an ordering rule.”** It lacks key, direction, tie-break, and consistency.
- **“Integer defines numeric meaning.”** Range, unit, precision, overflow, and domain scale can remain unknown.
- **“Security schemes define authorization.”** They describe credential mechanisms, not resource and field policy.
- **“Examples resolve ambiguity.”** They witness a rule; without a rule, other values remain undecided.
- **“Implementation-defined is harmless flexibility.”** It forces every consumer and tool to tolerate multiple outcomes.
- **“A decision table proves completeness.”** It proves coverage only for its declared variables and rows.
- **“A linter can approve semantics.”** It cannot judge domain meaning, safe recovery, or adequate scope.
- **“More findings mean worse review quality.”** Finding severity and closure matter more than counts.
- **“No findings proves no ambiguity.”** Report reviewed scope, artifact, methods, and limitations.

## Worked Examples

### Example 1

**Situation:** `limit` is optional with `maximum: 100`, but no default or minimum is stated. **Reasoning:** Test omission, zero, one, 100, and 101. Specify default 20, inclusive range 1–100, and `400` problem for invalid values. **Conclusion:** schema fragments become a complete parameter decision only with omission and failure behavior.

### Example 2

**Situation:** Results are “ordered by date.” **Reasoning:** Identify created versus modified, choose descending creation time, add ascending ID tie-break, and state consistency during pagination. **Conclusion:** a total, stable-enough ordering replaces an adjective.

### Example 3

**Situation:** Patch schema makes `nickname` optional and nullable. **Reasoning:** Define omission as unchanged, null as clear, empty string as invalid, ordinary string as replace, and unknown property as rejection. **Conclusion:** presence semantics belong to the operation, not type syntax alone.

### Example 4

**Situation:** `amount: 15` lacks unit. **Reasoning:** Decide that amount is a decimal currency value rather than minor units, require three-letter currency, define scale and rounding, and test overflow. **Conclusion:** number shape without unit and arithmetic policy is incomplete.

### Example 5

**Situation:** Create documents `201` and `400` only. **Reasoning:** Trace authentication, authorization, media type, payload size, domain conflict, quota, idempotency mismatch, and dependency failure; decide which are public and how clients recover. **Conclusion:** known failure space is part of the contract.

### Example 6

**Situation:** Two schemas in `oneOf` both accept `{id:"x"}`. **Reasoning:** Construct overlap witness, introduce a required discriminating tag or mutually exclusive constraints, and test zero/one/multiple matches. **Conclusion:** union syntax does not ensure unambiguous classification.

### Example 7

**Situation:** `202` says work completes “soon.” **Reasoning:** Add operation resource, allowed states, polling guidance, terminal success/failure, retention, cancellation, and explicitly state whether an upper bound exists. **Conclusion:** asynchronous acceptance needs an observation contract.

### Example 8

**Situation:** A retry after response loss creates two payments. **Reasoning:** Specify idempotency identity scope, payload mismatch response, concurrency behavior, retention, and replayed outcome; test one durable effect. **Conclusion:** retry safety requires effect identity and postconditions.

### Example 9

**Situation:** `GET /accounts/{id}` returns `403` for another tenant and `404` for absence. **Reasoning:** The difference reveals existence. Choose concealment policy, align timing, caches, errors, and list totals, and test all actor-resource relationships. **Conclusion:** authorization review includes information disclosure.

### Example 10

**Situation:** A Boolean decision table covers all eight triples of existence, visibility, and version freshness. **Reasoning:** Enumeration proves coverage only for those variables; deletion state and malformed validator remain outside the model. Record the limitation and add variables when risk requires. **Conclusion:** scoped completeness is useful when honestly bounded.

## Cross-Program Connections

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies requirements traceability and verification reasoning. [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies partitions, boundary witnesses, oracles, and coverage limits. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies authorization and disclosure review. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies time, partial failure, retries, consistency, and state reasoning. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) can automate lint and review workflows without owning domain decisions.

## References

1. OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/v3.2.0.html), including undefined and implementation-defined behavior and the normative object model, 19 September 2025. Checked 2026-09-01.
2. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), Internet Standard, June 2022. Checked 2026-09-01.
3. S. Bradner, [*RFC 2119: Key words for use in RFCs to Indicate Requirement Levels*](https://www.rfc-editor.org/rfc/rfc2119.html), BCP 14, March 1997; and B. Leiba, [*RFC 8174*](https://www.rfc-editor.org/rfc/rfc8174.html), May 2017. Checked 2026-09-01.
4. ISO/IEC/IEEE, [*29148:2018 Systems and software engineering—Life cycle processes—Requirements engineering*](https://www.iso.org/standard/72089.html), second edition, 2018. Checked 2026-09-01; a successor edition was under committee development, so the edition is stated explicitly.
5. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema Validation, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-validation), 16 June 2022. Checked 2026-09-01.
6. M. Nottingham, E. Wilde, and S. Dalal, [*RFC 9457: Problem Details for HTTP APIs*](https://www.rfc-editor.org/rfc/rfc9457.html), Standards Track, July 2023. Checked 2026-09-01.

## Exercises

### Exercise 1

Classify each defect: “recent,” no expired-cursor rule, two different defaults, and an explicitly permitted `200`/`202` alternative with defined handling. Explain the repair or justification.

### Exercise 2

Build a decision table for updating a resource across existence, visibility, validator presence, and validator freshness. Identify impossible states, public outcomes, and information-disclosure constraints.

### Exercise 3

Audit a `PATCH /profiles/{id}` contract for absent, null, empty, unknown, read-only, forbidden, concurrent, and retry behavior. Propose witnesses and closure evidence.

### Exercise 4

Review a cursor-paginated event API with mutable results, timestamp ordering, approximate totals, and cursor expiry. Produce precise rules without freezing internal storage design.

### Exercise 5

Design a review program for a previously released contract with 80 operations and three generated-client languages. Define passes, sampling, automation, prioritization, compatibility handling, closure, and honest reporting.

## Answers to the Exercises

### Answer 1

“Recent” is ambiguous: define time field, window or count, order, tie-break, and clock. Missing expired-cursor behavior is incomplete: define status/problem and restart recovery. Two defaults are inconsistent: choose one authority, update all projections, and assess consumers. The `200`/`202` alternative is intentional freedom only if conditions or allowed choice, meanings, response forms, and consumer handling are defined; otherwise it remains ambiguity.

### Answer 2

Start with 16 Boolean combinations, then note that freshness is meaningful only when a validator is present and the resource is visible. For absent or concealed resources, return the chosen non-disclosing `404` regardless of validator. For visible resources, missing required precondition yields `428` if that is policy; stale validator yields `412`; fresh validator permits update and returns a new validator. State how malformed validators fail and keep timing, cache, and problem detail from revealing concealed existence. Generate one witness per retained row and test mutual exclusion.

### Answer 3

Define omission as unchanged, null per-field as clear or invalid, empty values with explicit length rules, unknown request properties as reject or ignore, and read-only fields as rejected without mass assignment. Specify actor ownership and field capabilities, `If-Match` behavior, one transition per current version, and retry identity if the operation can be repeated after response loss. Witness each field class, cross-field rule, stale and concurrent requests, forbidden target, and duplicate retry. Close through schema/prose updates, examples, semantic diff, provider negative tests, authorization tests, and consumer parsing evidence.

### Answer 4

Define descending event-time order with immutable event ID tie-break, cursor bound to filters and order, and whether traversal is snapshot-like or may include duplicates/omissions under concurrent insertion. Keep cursor opaque; state expiry timestamp or maximum lifetime, invalid/expired problem type, and restart method. Label totals approximate with observation time and permitted error only if useful, or omit them. These rules constrain observable traversal while leaving indexes, storage engine, token encoding, and query plan internal.

### Answer 5

Pin the released and candidate artifacts, inventory consumers and incidents, and automate structure, references, schema/examples, links, math, code annotations, and semantic diffs over all operations. Run task, vocabulary, accepted/produced set, HTTP, state/time, retry, security, and operational passes. Include every risk class and client language in semantic sampling, then expand when a defect suggests a pattern. Prioritize disclosure, duplicate effects, incompatible wire behavior, and unrecoverable flows. Treat repairs as compatibility changes with migration where needed. Close only through authority, projections, tests, and re-review. Report exact operations sampled, deterministic checks, open findings, artifact digests, and limitations—never universal completeness.
