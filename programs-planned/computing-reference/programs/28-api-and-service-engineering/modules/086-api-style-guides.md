---
module_id: API-086
program: API & Service Engineering
level: 2
module_number: 86
title: API Style Guides
status: complete
last_verified: 2026-09-02
---

# API Style Guides

## One-Page Review

### Governing question

How should an organization turn standards, architecture decisions, consumer needs, and operational experience into a scoped, testable, evolvable API style guide that improves consistency without overriding protocol semantics or freezing bad decisions?

### Essential definitions

- An **API style guide** is a governed set of interface design rules, rationales, examples, and exception/change processes for a defined scope.
- A **profile** selects and constrains a protocol/specification for an organization or API family; it does not replace the underlying standard.
- A **normative rule** states an obligation or permission; an **informative explanation** supplies rationale, teaching, or examples.
- A **rule identifier** is a stable durable key used by documentation, linters, exceptions, review findings, and migration records.
- A **conformance claim** names the guide version, applicable scope, evaluated artifact/runtime evidence, and unresolved findings.
- An **exception** is a bounded, owned, expiring decision not to apply a rule; it is not an undocumented precedent.
- A **lintable rule** can be checked reliably from an identified artifact; a **judgment rule** needs human evidence and review.
- **grandfathering** preserves an existing behavior temporarily to avoid an unsafe breaking change while preventing new adoption.

### Central model, mechanism, or theorem

For API surface $a$, let $R(a)$ be rules applicable after protocol, API style, lifecycle state, exposure, and domain predicates are evaluated. Partition them into mandatory $M(a)$ and advisory $A(a)$. Conformance is not an average score:

$$
\operatorname{conforms}(a) \iff \left(\forall r\in M(a):\operatorname{pass}(a,r)\lor\operatorname{exception}(a,r)\right) \land \operatorname{evidenceFresh}(a).
$$

Advisory scores may prioritize improvements, but one violated security or compatibility MUST rule cannot be canceled by many naming passes. Every rule carries stable ID, strength, scope predicate, rationale, good/bad examples, check method, remediation, owner, introduction/version, and exception policy.

### Critical invariants

Protocol and security semantics outrank house style. A guide declares scope and precedence; REST, RPC, GraphQL, events, webhooks, and internal/public APIs receive appropriate profiles. Normative words are defined consistently. Rules do not contradict one another or require a breaking change without lifecycle analysis.

Automated checks report only what their inputs prove. Human review owns semantic resource boundaries, consumer tasks, authorization, error meaning, compatibility, and operational behavior. Findings identify rule/version/location/evidence and support suppression only through recorded exceptions. Guide changes are versioned, impact-assessed, tested against a representative corpus, communicated, and adopted through safe migrations.

### Common failures

Copying another company’s guide without context; mixing protocol fact with preference; one guide for every interface style; undocumented precedence; lowercase “must” ambiguously normative; rules without rationale/examples; contradictory rules; vague “RESTful” requirements; linting syntax while missing semantics; treating linter score as quality; unstable rule IDs; false-positive floods; blanket suppressions; permanent exceptions; retroactive enforcement that breaks clients; formatting churn mixed with behavior changes; guide repository detached from templates/tooling; no owner or change process; drift among prose, linter, and examples; and measuring compliance rather than consumer outcomes.

### Compact example

Rule `HTTP-ERR-001` says public JSON HTTP APIs MUST return an RFC 9457 problem details document for governed application errors, with an allowlisted stable `type`; it excludes streaming responses and documents security redaction. The linter can confirm the OpenAPI media type/schema reference, but reviewers/test evidence confirm status mapping, stable type semantics, safe detail, and runtime behavior. A legacy API receives a dated exception plus compatibility migration. **Conclusion:** one rule joins scope, semantics, automation, judgment, and lifecycle evidence.

### Connections

[API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md) defines what rules govern. [OpenAPI Structure](023-openapi-structure.md) provides a lintable artifact. [Choosing an Interface Style](060-choosing-an-interface-style-from-interaction-semantics.md) prevents REST rules from leaking into unsuitable protocols. [Compatibility](081-backward-and-forward-compatibility.md) and [Deprecation and Sunset](084-deprecation-and-sunset.md) constrain adoption. The next modules apply the guide in design reviews, registries, product ownership, and independent evolution.

## Governing Question

What belongs in an API style guide, which authority and scope does each rule have, what can tools prove, how are exceptions and guide changes governed, and how can consistency be improved without sacrificing semantics, compatibility, security, or justified domain differences?

## Why This Matters

Consumers learn an API partly by transferring expectations from neighboring APIs. Consistent resource names, pagination, errors, time formats, idempotency, concurrency controls, authentication placement, and lifecycle signals lower accidental cognitive load. Providers reuse review knowledge, generators, policies, SDK behavior, telemetry, and operational runbooks.

Consistency is not sameness for its own sake. A synchronous resource API, a command-oriented RPC surface, a GraphQL graph, a webhook, and an ordered event stream have different semantics. Forcing all of them into plural nouns and HTTP CRUD can make behavior less honest. Even within HTTP, protocol standards define method, status, cache, conditional, and representation semantics that a house guide must not rewrite.

Guides also create organizational power. A vague rule can block delivery, impose one team’s preferences, or trigger breaking “cleanup.” An automated gate can produce false authority. Conversely, an exception process without accountability turns every rule optional. Durable governance makes authority, evidence, ownership, appeal, and change explicit.

A good guide captures costly lessons once, close to executable artifacts and workflows. It lets teams spend review time on domain boundaries and risk rather than repeatedly debating casing. It remains a living product: scoped to consumers, tested against real APIs, versioned, taught, measured, and revised when evidence changes.

## Prerequisites and Retrieval

Retrieve [HTTP Methods and Their Semantics](002-http-methods-and-their-semantics.md), [Status Codes and Error Meaning](003-status-codes-and-error-meaning.md), [URI Design](013-uri-design.md), [Filtering, Sorting, and Pagination](017-filtering-sorting-and-pagination.md), [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [OpenAPI Structure](023-openapi-structure.md), [Reviewing a Contract for Ambiguity and Incompleteness](030-reviewing-a-contract-for-ambiguity-and-incompleteness.md), [Choosing an Interface Style from Interaction Semantics](060-choosing-an-interface-style-from-interaction-semantics.md), [Backward and Forward Compatibility](081-backward-and-forward-compatibility.md), and [Deprecation and Sunset](084-deprecation-and-sunset.md).

Retrieve the current protocol standards and organization architecture decisions; existing API specifications and production behavior; consumer research/support incidents; security/privacy/accessibility policy; SDK/generator/templates; linter rules/configuration; exception and review history; compatibility/deprecation policy; ownership/catalog data; telemetry; and representative conforming, legacy, internal, partner, public, REST, RPC, GraphQL, event, and webhook surfaces.

## Learning Objectives

After completing this module, you can:

1. distinguish protocol standards, organization profiles, domain conventions, API decisions, and examples;
2. define guide scope, precedence, normative vocabulary, and rule applicability precisely;
3. write durable rules with IDs, rationale, examples, verification, remediation, ownership, and exceptions;
4. cover resource/operation, schema, error, collection, reliability, security, lifecycle, documentation, and observability conventions coherently;
5. separate mechanically lintable properties from semantic and runtime judgment;
6. design deterministic findings, severity, baselines, suppressions, and exception records;
7. test rule interactions and tools against conforming and adversarial API corpora;
8. evolve a guide through versioning, impact analysis, compatibility-safe migration, and communication;
9. govern grandfathered APIs and bounded exceptions without creating permanent ambiguity; and
10. measure whether the guide improves consumer and provider outcomes rather than maximizing superficial compliance.

## Core Exposition

### Define purpose, audience, and scope

Start with outcomes: predictable consumer experience, semantic correctness, security, compatibility, operational diagnosability, and efficient delivery. “Make every API look identical” is not sufficient purpose.

Name audiences: designers, implementers, reviewers, security teams, SDK/tool authors, documentation writers, operators, and consumers. Give each a path through the guide. A 400-page reference without task-oriented entry points is not usable governance.

State applicability as predicates: organization/business unit, exposure (public/partner/internal), protocol/interface style, lifecycle state, data/risk class, and guide version. Record exclusions. A JSON HTTP profile does not silently govern Protobuf field evolution; a public compatibility rule may be stricter than an experimental internal surface.

Avoid “REST” as an unexamined scope label. Say whether a rule assumes HTTP resources, OpenAPI, JSON, synchronous request/response, browser access, or public consumers.

### Establish authority and precedence

Use layers. First are protocol/format/security/legal standards. Second are organization-wide architecture and product policies. Third is the selected API-family profile. Fourth is domain convention. Fifth is an API-specific decision or approved exception.

Document precedence. A house preference cannot redefine HTTP `GET` as unsafe or assign a standard status code a contradictory meaning. Domain policy may select a narrower behavior when the guide explicitly allows it. An exception cannot waive law or nondelegable security control.

Distinguish incorporation from restatement. Link to canonical specifications and state the local choice; do not paraphrase hundreds of standard requirements into a fork that silently becomes stale. Pin or name editions when semantics depend on a version and maintain a verification date.

When authorities conflict, open a governed issue with exact clauses, affected APIs, consumer impact, and an interim decision. “The linter says so” does not resolve precedence.

### Use normative language deliberately

RFC 2119 defines uppercase requirement keywords; RFC 8174 clarifies that they have the special BCP 14 meaning only when uppercase as shown. A guide can adopt that convention explicitly. Use MUST/MUST NOT for requirements whose violation is unacceptable within scope, SHOULD/SHOULD NOT when valid exceptions can exist but implications must be understood, and MAY for genuine options.

Do not turn taste into MUST. High mandatory-rule volume creates exception theater and hides critical controls. State actor and condition: “Public JSON HTTP operations returning a governed application error MUST…” is testable; “errors must be consistent” is not.

Separate normative sentence from rationale, examples, and implementation advice. Examples never narrow or broaden the rule invisibly. Define terms in one glossary and avoid synonyms such as identifier/key/name unless differences are intentional.

### Design each rule as a durable record

Give each rule a stable semantic identifier, not a document section number. Include title, normative statement, scope predicate, rationale/consumer consequence, positive and negative examples, verification method/input, finding severity, remediation, exception eligibility, rule owner, introduced/changed/deprecated guide version, and related standards/rules.

IDs survive reordering and wording changes. Never reuse a retired ID for different semantics. Tool output, pull-request comments, waivers, dashboards, training, and migrations can then refer to the same decision.

Make bad examples fail for one explained reason. Large examples with several violations confuse both learners and linter fixtures. Include boundary cases and counterexamples, not only ideal happy paths.

For judgment rules, define required evidence: task model, authorization matrix, state transition, compatibility classification, threat model, load/retry budget, or owner approval. “Manual” should not mean subjective taste.

### Cover the interface as a coherent system

Resource/operation rules address consumer tasks, identifiers, URI/name patterns, method semantics, commands, long-running work, bulk behavior, and boundaries. Schema rules address types, requiredness, null/absence, defaults, enum openness, units, time, money, localization, polymorphism, and constraints.

Collection rules align filtering, sorting, pagination/cursors, search, limits, total counts, consistency, and empty results. Error rules align transport status with stable machine-readable application meaning, correlation, safe detail, field violations, retryability, and documentation. RFC 9457 is one standard profile for HTTP problem details, not a reason to expose internals.

Reliability rules cover idempotency, conditional updates, concurrency, timeouts/deadlines, retry signals, quotas, asynchronous acceptance, delivery/acknowledgment, and replay. Security/privacy rules cover authenticated context, authorization boundaries, least privilege, enumeration, overposting, credentials, sensitive fields, logging, and data minimization.

Lifecycle rules cover compatibility, version selection, deprecation/sunset, consumer evidence, and support. Documentation/operations rules cover descriptions, examples, contact/ownership, SLOs, correlation, health, observability fields, and incident/deprecation signals. Check cross-rule consistency: pagination errors, auth errors, and long-running operations still follow common error and lifecycle policy.

### Profile rather than clone external guides

Google’s AIPs organize design guidance as individual proposals and explicitly distinguish general and service-specific material. Zalando publishes RESTful API and event guidance with rule identifiers and normative conventions. Microsoft’s former general REST guideline now redirects Azure and Graph teams to separate documents. These are valuable evidence and patterns, not automatically your policy.

For each imported idea, record why it fits local consumers, protocols, tooling, risk, and lifecycle. Preserve upstream attribution and track the source edition. Rewrite into local terms only when necessary, and test interactions with existing rules.

Do not combine the strictest clause from every guide. The result can be internally contradictory or impossible for your toolchain. Adopt the smallest coherent profile that solves observed problems, then evolve it with evidence.

### Separate specification, policy, and examples

OpenAPI describes an HTTP API surface in a machine-readable form, but the OpenAPI Specification does not choose your resource naming, pagination, authorization model, or compatibility policy. A style guide constrains how your organization uses it. A linter evaluates selected representable constraints. Production tests and review evaluate behavior.

Keep one source of truth for each layer. Generate rendered guide navigation and tool metadata from rule records when feasible, but do not pretend prose can be fully generated from schemas. Test published examples as fixtures so they do not drift from the linter or current spec edition.

Templates accelerate the preferred path but remain subordinate to rules. A generated starter that violates the guide destroys trust faster than missing automation.

### Classify what automation can prove

Syntax/shape checks can often verify paths, operation IDs, schema names, required descriptions, response declarations, media types, reusable components, forbidden header names, and presence of lifecycle/security annotations. Semantic checks may inspect known patterns but have limits.

A static OpenAPI linter cannot prove that `GET` has no side effect, authorization enforces object access, cursor pagination is stable, error detail is safe, retry behavior matches documentation, or a resource boundary matches consumer tasks. It can flag evidence gaps or suspicious shapes; human review/runtime tests must close them.

Every automated rule declares accepted input/version, decision procedure, diagnostic location, severity, remediation, and known false positives/negatives. Deterministic results matter: the same artifact/config/tool version should yield the same findings.

Run rule tests with positive, negative, boundary, and malformed fixtures. Test the whole rule set against a representative corpus before enforcing it; rule interactions and parser/spec-version changes create surprises.

### Design findings, baselines, and gates

A finding includes rule ID and version, artifact location, actual condition, expected condition, consequence, remediation link, and whether exception is possible. Avoid duplicate cascades when one root error causes many downstream failures.

Severity maps to policy: blocking error, required remediation with deadline, warning, or information. Do not map every MUST mechanically to build failure if the tool is uncertain; improve the rule/evidence model first.

For legacy adoption, capture an immutable baseline of existing findings. Gates can block newly introduced violations while teams retire debt deliberately. Baselines do not make findings compliant and must not hide a changed line that worsens risk.

Suppressions name the stable rule and smallest artifact scope and link to an exception record. Inline “ignore all” comments without owner/rationale/expiry become an alternative shadow guide.

### Govern exceptions and appeals

An exception records API/surface, rule ID/version, exact deviation, rationale and rejected alternatives, consumer/security/compatibility impact, compensating control, owner/approver, evidence, issue link, start/expiry/review date, and removal/migration condition.

Some rules are non-waivable within a governance body’s authority; say which and why. Others permit local trade-offs. Approval level follows risk, not team seniority or deadline pressure.

Aggregate exceptions by rule and cause. Many similar exceptions indicate a bad rule, missing scope predicate, missing platform capability, or systematic legacy constraint. Fix the durable source rather than renew waivers forever.

Provide appeal and response SLOs. Governance that cannot resolve ambiguity quickly encourages bypass. Publish decisions and sanitized precedents, but do not let one exception silently become a universal rule.

### Evolve the guide as a product

Version the guide and its machine rules together. Classify changes: clarification with no normative change, additive advisory rule, new mandatory rule, tightened applicability, changed semantics, deprecation/removal, or correction to align with higher authority.

Before release, compute affected artifacts/teams, run the new rules against the corpus, review false positives, assess compatibility and tooling/template changes, and produce migration guidance. A guide change can be breaking for providers even when no wire contract changes.

Use proposal review for consequential rules. Include problem evidence, alternatives, consumer research, standard citations, examples, tooling feasibility, rollout, and success/reversal criteria. Record decisions durably.

Do not rewrite history silently. Publish changelog, effective dates, support windows for tool versions, and what existing APIs must do. Guide removal also needs migration because tooling and exception records depend on rule IDs.

### Adopt without breaking consumers

New APIs can target the current profile before launch. Existing APIs require compatibility classification. A naming inconsistency may be less harmful than renaming a shipped field. Freeze new use of the legacy form, support aliases or additive replacements where sound, deprecate with consumer evidence, and remove only through lifecycle policy.

Separate formatting-only spec normalization from wire/runtime changes. Generated diffs can conceal requiredness, default, enum, or status changes. Review semantic diffs and production behavior.

Offer paved paths: templates, reusable schemas, generators, examples, migration recipes, office hours, and actionable diagnostics. Train reviewers and platform owners, not only API teams.

Roll out observation, warning, changed-lines blocking, then broader enforcement according to risk. Emergency security/correctness rules may accelerate but still require scoped authority, evidence, communication, and remediation support.

### Measure outcomes and maintain coherence

Track time to first successful consumer call, support incidents, ambiguity/rework findings, review lead time, SDK/documentation defects, compatibility incidents, unknown consumers, exception age/concentration, false-positive/appeal rate, remediation time, and adoption by applicable scope.

Raw pass percentage is diagnostic, not the goal. Teams can maximize it by avoiding documented surfaces, suppressing checks, or satisfying syntax while behavior remains unsafe. Pair conformance with consumer and operational outcomes.

Assign guide product ownership and domain rule owners. Schedule source/spec refresh, broken-link/example tests, rule/tool parity checks, exception review, corpus analysis, and consumer feedback. Archive superseded editions while keeping old conformance/exception records interpretable.

Use incidents and design-review findings as input, but do not encode every one-off incident into a global MUST. Confirm recurrence, generality, enforceability, and net benefit. A compact coherent guide is more authoritative than a contradictory encyclopedia.

## Definitions and Notation

Let $G_v$ be guide version $v$ and $R(a)$ the rules whose scope predicates apply to API surface $a$. Let $M(a)\subseteq R(a)$ be mandatory rules and $A(a)=R(a)\setminus M(a)$ advisory rules. For rule $r$, $p(a,r)$ means passed with adequate evidence, and $x(a,r)$ means a valid unexpired exception covers the exact surface.

Conformance is $C(a)=\bigwedge_{r\in M(a)}(p(a,r)\lor x(a,r))$ plus fresh evidence. A weighted advisory measure $s=\sum w_rp_r/\sum w_r$ may prioritize work when its denominator is positive, but cannot replace $C$.

A **profile** is a scoped selection/constraint over a protocol or description standard. **Precedence** orders conflicting authorities. **Applicability** evaluates a rule’s scope predicate. A **baseline** records existing findings for differential adoption. A **suppression** is a tool reference to an approved exception, not the exception itself.

## Mechanisms, Invariants, or Proof Structure

**Precedence argument.** Protocol semantics define interoperable meaning. If a lower-level house rule contradicts them, conforming external participants interpret the standard rather than the private rewrite. Therefore protocol/security/legal authority must outrank style preference, and conflicts must be resolved explicitly.

**Conformance counterexample.** An API passes 99 naming/documentation checks but violates one mandatory object-authorization rule. Its average is 99%, yet it exposes another tenant’s data. Therefore average rule score cannot establish mandatory conformance; mandatory obligations require conjunction or explicit valid exception.

**Automation boundary argument.** A linter observes its artifact, configuration, and algorithm. Two implementations can share the same OpenAPI declaration while one performs side effects on `GET` and the other does not. Therefore artifact linting alone cannot prove runtime semantic behavior; contract/runtime/security evidence is necessary.

**Migration invariant.** A shipped inconsistent name can be a consumer dependency. Renaming it solely to satisfy a new guide changes the contract and may break consumers. Therefore guide adoption is constrained by compatibility and deprecation evidence; grandfathering plus prevention of new use can be safer than immediate cosmetic uniformity.

Operational invariants are: scope and precedence explicit; normative strength intentional; stable rule identity; one coherent authority per layer; lint claims bounded by evidence; exceptions owned and expiring; guide/tool/examples version-aligned; changes impact-tested; shipped contracts compatibility-protected; and outcome evidence paired with conformance.

## Alternatives and Trade-Offs

One enterprise guide improves shared tooling and learning but may erase protocol/domain differences. Fully federated guides fit domains but fragment consumer experience. Use a small common core plus explicit protocol/product profiles and governed domain extensions.

Strict automated gates provide fast consistency but amplify false positives and optimize for machine-visible shape. Human-only review understands context but is slow and inconsistent. Automate deterministic mechanics; require structured evidence and accountable review for semantics.

Very detailed rules reduce ambiguity but become hard to navigate and update. Principle-only guides are readable but produce inconsistent decisions. Pair concise normative rules with rationale, focused examples, and linked deep guidance.

Immediate enforcement prevents new debt but can halt legacy delivery or induce breaking changes. Permanent grandfathering preserves compatibility but entrenches divergence. Differential gates plus risk-ranked migration and expiry balance both.

Forking external guidance gives local control but loses upstream corrections. Direct adoption reduces maintenance but may not fit scope/tooling. Maintain an explicit local profile and source map; incorporate only justified rules.

Central governance creates consistency and neutral appeals but can become a bottleneck. Team ownership moves quickly but risks local bias. Give domain owners proposal authority within a common precedence, evidence, and review framework.

## Failure Modes and Misconceptions

- “A style guide is a naming guide.” Naming is a small part of behavioral consistency.
- “More uniform is always better.” Honest protocol/domain semantics can require variation.
- “Our guide replaces HTTP/OpenAPI.” It profiles them and cannot rewrite their meaning.
- “Another company already solved this.” Its consumers, history, risk, and tools differ.
- “Every recommendation should be MUST.” Excess strength creates meaningless exceptions.
- “The example is normative.” Only explicitly marked rule text defines obligation.
- “The linter proves API quality.” It proves bounded properties of its inputs.
- “No finding means runtime conformity.” Side effects, authorization, and operational behavior may be invisible.
- “A 95% score passes.” One fatal mandatory violation can dominate.
- “Suppress means approved.” Suppression must resolve to a scoped exception record.
- “Exceptions weaken governance.” Bounded evidence exposes real trade-offs; hidden divergence weakens it.
- “Legacy must be cleaned up now.” Cosmetic consistency does not justify consumer breakage.
- “Guide changes are not breaking.” Provider workflows, tooling, and approvals can break.
- “One profile fits REST, RPC, GraphQL, and events.” Their interaction semantics differ.
- “Generated templates guarantee conformance.” Templates can drift and behavior can diverge.
- “Compliance percentage is success.” Consumer, security, compatibility, and delivery outcomes matter.

## Worked Examples

### Example 1

Rule `HTTP-METHOD-001` says a governed `GET` MUST be safe according to HTTP semantics. The OpenAPI linter flags suspicious operation metadata, but runtime tests and review establish absence of intended state change. A house convention cannot redefine `GET` as a command.

### Example 2

A public JSON API uses `snake_case`; an acquired partner API ships `camelCase`. Renaming shipped fields would break consumers. The exception freezes legacy names, requires `snake_case` for additive fields only if mixed casing is acceptably documented, and schedules an intentionally versioned migration rather than a mass rewrite.

### Example 3

One linter rule requires pagination on every array response, including a bounded seven-day enum-like calendar. Scope is corrected from “array” to “unbounded/evolving collection,” eliminating false positives and unnecessary cursor complexity.

### Example 4

An API passes 99 low-risk style checks but fails object-level authorization. The conjunction model marks it nonconforming despite a 99% score; release remains blocked until the control passes or the non-waivable security authority changes.

### Example 5

Rule `HTTP-ERR-001` checks an OpenAPI `application/problem+json` response. Review finds production sends stack traces in `detail`. Schema conformance passed, but security/runtime conformance failed; the finding model keeps those claims separate.

### Example 6

A GraphQL team is told to use plural URI nouns. Applicability evaluation excludes the rule because the surface is a graph endpoint; GraphQL-specific schema, pagination, error, authorization, and evolution rules apply instead.

### Example 7

A linter upgrade produces 2,000 existing warnings. The organization records a reviewed baseline, blocks new violations on changed surfaces, fixes critical rules first, tracks owner/expiry, and prevents a blanket ignore file from becoming permanent policy.

### Example 8

Fifteen exceptions to a “no custom operations” rule cover legitimate long-running domain commands. Governance revises the REST profile to define command/action semantics and migration rules. Similar exceptions revealed a deficient rule rather than fifteen deficient teams.

### Example 9

A proposal changes timestamps from ambiguous local strings to RFC 3339 instants. New fields follow the rule; existing fields gain additive replacements, consumer migration evidence, deprecation, and eventual removal. The guide does not authorize an in-place type change.

### Example 10

Metrics show 98% lint pass rate, yet consumer onboarding takes three days because authentication examples and test credentials are unusable. Guide ownership prioritizes executable onboarding and credential guidance; outcome measurement corrects the vanity metric.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies architecture decisions, boundary design, quality attributes, and governance structure for common cores and profiles.

[Software Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies static-analysis validity, test design, false-positive control, quality models, and evidence beyond a score.

[Security Engineering](../../25-security-engineering/ROADMAP.md) establishes non-waivable controls, threat modeling, authorization, sensitive error/log behavior, and risk-ranked exceptions.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects requirements, interface control, configuration baselines, verification evidence, change control, and lifecycle traceability.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) constrains rules for retries, idempotency, ordering, deadlines, partial failure, consistency, and asynchronous interaction.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) operationalizes guides through templates, generators, linting, catalog ownership, CI gates, paved paths, telemetry, and support.

## References

1. IETF, [RFC 2119: Key Words for Use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119.html).
2. IETF, [RFC 8174: Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174.html).
3. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
4. IETF, [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html).
5. OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).
6. Google, [API Improvement Proposals: General AIPs](https://google.aip.dev/general).
7. Microsoft, [Azure REST API Guidelines](https://github.com/microsoft/api-guidelines/tree/vNext/azure).
8. Zalando, [RESTful API and Event Guidelines](https://opensource.zalando.com/restful-api-guidelines/).

## Exercises

### Exercise 1

Design the layered structure, precedence, and applicability model for an organization with public REST/JSON, internal gRPC, partner GraphQL, webhooks, and events. Identify the common core and profile-specific rules.

### Exercise 2

Write a complete rule record for stable error semantics, including ID, normative text, scope, rationale, examples, automated and human verification, severity, remediation, exception policy, ownership, and version metadata.

### Exercise 3

A public API has 96 passing advisory checks, three mandatory passes, and one failed mandatory object-authorization rule. Compute an undifferentiated pass percentage, then evaluate the conjunction conformance model and explain the difference.

### Exercise 4

Plan adoption of a new timestamp and field-naming profile across 120 shipped APIs with 3,400 existing findings, several SDK generators, public consumers, and an unreliable linter rule. Preserve compatibility while stopping new debt.

### Exercise 5

Design an evidence dashboard and maintenance cycle that detects guide/tool/example drift, exception debt, false-positive harm, shallow compliance, and consumer outcomes without turning the pass rate into a target.

## Answers to the Exercises

### Answer 1

Place protocol/format/security/legal authorities first: HTTP/OpenAPI/JSON, Protobuf/gRPC, GraphQL, and event/webhook specifications as applicable. Add an organization core for ownership, security/privacy, compatibility, normative vocabulary, stable rule IDs, documentation, observability, evidence, exceptions, and lifecycle. Create profiles for public REST/JSON resources and HTTP semantics; internal gRPC service/method/deadline/status/schema evolution; partner GraphQL schema/pagination/errors/cost/authorization; webhook signing/delivery/retry/idempotency; and event schema/topic/key/ordering/delivery/replay. Domain extensions may narrow choices without contradicting higher layers. Applicability evaluates exposure, protocol, lifecycle, and risk. API-specific decisions are last; exceptions cannot waive nondelegable authority. Publish precedence/conflict resolution and never apply URI-noun rules to GraphQL or HTTP status rules to an event payload.

### Answer 2

Use stable ID `HTTP-ERR-001`, title “Governed problem details,” and normative text: “Public JSON HTTP operations in this profile that return governed application errors MUST use `application/problem+json` conforming to RFC 9457; `type` MUST be a stable allowlisted identifier, and fields MUST NOT expose secrets or internals.” Scope excludes streaming/protocol-level responses and lists inherited security rules. Rationale is predictable machine handling and safe diagnosis. Good/bad fixtures isolate media type/schema, stable types, status mapping, extensions, and redaction. Static verification checks declared media/schema/type registry; contract/runtime/security tests check actual status/body, stability, retry meaning, and disclosure. Severity is blocking for new public APIs. Remediation links reusable schema and migration recipe. Exception requires exact operations, consumer/security analysis, compensating mapping, owner/approver, expiry, and migration. Record rule owner, RFC/OpenAPI sources, introduced guide/tool versions, and non-waivable redaction clause.

### Answer 3

An undifferentiated count reports $99/100=99\%$ because 96 advisory plus three mandatory checks pass out of 100. That number hides the failed authorization obligation. With $M(a)$ containing four mandatory rules, one member has neither pass nor valid exception, so $\bigwedge_{r\in M(a)}(p\lor x)$ is false: the API does not conform and release is blocked. Advisory percentage can order later work but cannot compensate for a mandatory security failure. The report must also confirm evidence freshness; even four stale “passes” would not establish current conformance.

### Answer 4

First repair and fixture-test the unreliable linter; do not gate on evidence known to be noisy. Inventory APIs, owners, exposure, contracts, generators, consumers, current timestamp/name semantics, and compatibility risk. Snapshot reviewed findings with rule/tool versions. Apply the new profile immediately to unshipped APIs and new compatible fields; use changed-surface gates to stop avoidable debt. Do not rename or retype shipped fields in place. Generate additive replacement fields/types, dual-read/write or mapping where semantically safe, updated SDKs/examples, and semantic-diff tests. Migrate consumers with evidence, deprecate, and remove through policy. Rank 3,400 findings by mandatory risk and affected consumers rather than raw count. Give every baseline/exception owner, review/expiry, remediation condition, and visible status; measure false positives, compatibility incidents, and consumer onboarding, not only finding burn-down.

### Answer 5

Version the guide, rule metadata, linter, templates, generators, examples, and evaluated artifacts. Continuously run positive/negative/boundary/malformed fixtures plus a representative API corpus; alert on rule result changes, broken links, untested examples, guide/tool rule-ID mismatch, parser/spec upgrades, and stale source verification. Report applicable surfaces, fresh mandatory conjunction, advisory distribution, new versus baselined findings, suppressions linked to valid exceptions, expiry/age/renewal/concentration by rule and cause, appeal outcomes, false-positive/negative samples, and remediation time. Pair these with time to first consumer success, support/design rework, compatibility/security incidents, SDK/doc defects, review lead time, and unknown ownership. Review monthly operational signals and expiring exceptions, quarterly corpus/outcomes and rule ownership, and on every standards/tool release. Do not rank teams by pass percentage; investigate gaming, missing artifacts, blanket suppression, and high syntax scores with poor runtime evidence.
