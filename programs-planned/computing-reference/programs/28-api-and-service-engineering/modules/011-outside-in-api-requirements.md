---
module_id: API-011
program: API & Service Engineering
level: 1
module_number: 11
title: Outside-In API Requirements
status: complete
last_verified: 2026-09-01
---

# Outside-In API Requirements

## One-Page Review

### Governing question

How do we derive a testable API contract from consumer goals, operating conditions, and failure consequences before implementation choices distort the problem?

### Essential definitions

- An **actor** is a person, software client, operator, or external system with a goal and relevant capabilities.
- An **outcome** is the externally meaningful state or information the actor needs, not an endpoint or database action.
- A **scenario** is a concrete interaction under stated preconditions, stimulus, observable response, and postcondition.
- A **requirement** is a necessary, verifiable property or constraint; a preference is negotiable and must not masquerade as one.
- An **acceptance oracle** decides from observable evidence whether a requirement is satisfied.
- A **quality attribute** constrains behavior such as latency, availability, privacy, accessibility, or recoverability.
- An **assumption** is a condition relied upon but not controlled by the API; it needs an owner and a failure response.

### Central model, mechanism, or theorem

Let $R$ be the set of requirements and $S$ the set of acceptance scenarios. Define coverage relation $C\subseteq R\times S$, where $(r,s)\in C$ means scenario $s$ can falsify or support requirement $r$ using observable evidence. Every mandatory requirement needs at least one normal, boundary, or failure scenario, but coverage does not prove the requirements are complete or the implementation correct.

### Critical invariants

State consumer outcomes before resources and methods. Separate domain policy from HTTP mechanism and implementation. Quantify quality thresholds with measurement boundaries. Specify errors and ambiguous outcomes as carefully as success. Record actor, precondition, stimulus, observable result, postcondition, priority, rationale, source, and acceptance evidence. Trace every contract element to a need; reject speculative fields and operations.

### Common failures

Starting from database tables; asking only for a list of endpoints; encoding one UI's click sequence as the domain contract; writing “fast,” “secure,” or “user-friendly” without an oracle; omitting retries, concurrency, authorization, pagination, and partial failure; confusing authentication with permission; treating an OpenAPI document as the requirements source; and accepting mutually inconsistent stakeholder wishes.

### Compact example

“Create `POST /orders`” is a design decision. “An authenticated buyer can submit a priced basket once, learn whether it was accepted within two seconds, and safely recover after a lost response without duplicate fulfillment” is an outside-in requirement. It exposes identity, idempotency, latency, error, and recovery questions before choosing a path or representation.

### Connections

HTTP semantics constrain later design choices but do not supply business requirements. Resource identification, operation design, representation schemas, compatibility, security, reliability, and testing all consume the requirement model established here. Requirements engineering supplies elicitation and traceability discipline.

## Governing Question

What must an API let its consumers accomplish, under which constraints and failures, and what observable evidence will distinguish satisfaction from wishful thinking?

## Why This Matters

An API is a long-lived boundary between independently changing systems. Once clients depend on names, meanings, timing, errors, permissions, and recovery behavior, implementation details become expensive public commitments. A technically valid HTTP exchange can still fail the consumer: a payment might be duplicated, a search might omit results silently, or a timeout might leave the outcome unknowable.

Outside-in analysis starts with actors and outcomes, then works inward toward interaction semantics. It delays path, method, schema, storage, and framework decisions until the problem is explicit enough to compare alternatives. This is not “design by committee.” It is disciplined discovery of obligations, conflicts, assumptions, and evidence.

ISO/IEC/IEEE 29148:2018 defines requirements-engineering processes and characteristics of requirements. It remains the published edition, while a third-edition DIS was under development when checked on 2026-09-01; this chapter relies only on durable concepts common to the published scope. RFC 9110 defines the HTTP semantics that later realize many interaction choices. OpenAPI Specification 3.2.0, published 19 September 2025 and checked on 2026-09-01, defines a machine-readable interface description; it can record a chosen contract but does not discover whether that contract solves the consumer's problem.

## Prerequisites and Retrieval

Retrieve resources, representations, HTTP methods, status codes, idempotency, caching, authentication versus authorization, timeouts, and distributed partial failure. Recall that a client observes messages and elapsed time, not internal commits directly. Be able to distinguish a goal, a mechanism, an implementation, a guarantee, and evidence.

## Learning Objectives

By the end of this module, you should be able to:

1. identify actors, outcomes, constraints, assumptions, and failure consequences;
2. convert vague wishes into atomic and falsifiable requirements;
3. write normal, boundary, failure, recovery, and abuse scenarios;
4. quantify quality attributes with explicit measurement boundaries;
5. separate domain obligations from HTTP and storage decisions;
6. detect conflicts, hidden coupling, and speculative surface area; and
7. build traceability from stakeholder evidence through acceptance scenarios to contract elements.

## Core Exposition

### Begin with actors and outcomes

Name actors by capability and responsibility, not by screen or organizational chart. “Warehouse scanner,” “partner reconciliation client,” and “on-call operator” reveal different credentials, latency, connectivity, and recovery needs. “Mobile user” is too broad if offline behavior and accessibility matter. A backend service can be an actor even when no human directly initiates its requests.

For each actor, ask what externally meaningful outcome is needed and what happens if it is late, duplicated, stale, disclosed, or unavailable. “Submit an order” is incomplete until the analysis states whether acceptance reserves stock, whether price can change, how a caller learns the durable outcome, and what safe recovery means after a lost response.

Avoid endpoint language during initial discovery. “The client calls `/validate` and then `/save`” embeds orchestration and race conditions. Ask instead: what decision must be made, what facts support it, which party owns the decision, and what must remain true between decision and effect?

### Gather evidence, not just opinions

Use interviews, observation, support incidents, existing traffic, regulations, contracts, threat models, and operational postmortems. Stakeholder statements are evidence of a need, not automatically the final requirement. A requested field may be a workaround for a missing workflow. A current client limitation may be temporary. A legal obligation needs authoritative interpretation and jurisdictional scope rather than folklore.

Record source, rationale, confidence, owner, and unresolved questions. Separate **fact** (“partner files arrive once daily”), **assumption** (“the partner clock is accurate”), **constraint** (“retention is seven years”), **policy** (“only owners may cancel”), and **design choice** (“use `DELETE`”). This prevents a provisional implementation idea from acquiring false authority.

### Write atomic, falsifiable requirements

A useful requirement states one obligation with a clear subject, condition, behavior, and observable result. Replace “the API should be fast and reliable” with separate claims such as “for accepted read requests under the declared load profile, 99% of server-observed response-header latencies are at most 300 ms over each rolling 30-minute window.” The threshold is still a policy choice, but it now has a population, boundary, statistic, and interval.

Use normative force deliberately. “Must” denotes a mandatory obligation; “should” needs a documented exception policy; “may” grants permission. Avoid conjunctions that hide multiple tests, pronouns with unclear referents, subjective adjectives, and absolute claims that the system cannot control. “Never loses data” is not testable without defining data, acknowledged states, fault model, retention, and evidence.

Each requirement needs an acceptance oracle. An oracle may inspect HTTP messages, authoritative operation state, audit records, metrics collected at a defined boundary, or controlled fault-injection results. A unit test of a handler is not evidence that a multi-service recovery obligation holds.

### Model scenarios across the outcome space

Write a scenario with actor, preconditions, stimulus, response, postcondition, and evidence. Cover the normal path, empty and maximum inputs, invalid syntax, domain rejection, unauthenticated and unauthorized actors, concurrency, retries, dependency failure, timeout before and after possible commit, cancellation, and recovery. Not every API needs every case, but omissions should be decisions rather than accidents.

Use examples to expose ambiguity. If “cancel an order” is requested, ask about already shipped, concurrently fulfilled, previously cancelled, unknown, and inaccessible orders. Ask whether repeated cancellation is safe, which outcome is disclosed to an unauthorized caller, and whether cancellation is immediate or an asynchronous request.

Scenario tables are models, not exhaustive proofs. Partition the state space by distinctions that change obligations. Boundary-value and adversarial cases are especially valuable because happy paths rarely expose ownership, timing, or information-disclosure errors.

### Quantify quality attributes honestly

Latency requirements need start and end points, traffic population, percentile or maximum, observation window, load, geography, payload size, cache state, and excluded failures. Availability needs the measured operation, successful response definition, time window, planned-maintenance policy, and dependencies. Throughput without concurrency and latency constraints can reward a system that queues work indefinitely.

Privacy and security requirements identify protected assets, principals, actions, trust boundaries, disclosure rules, retention, and audit evidence. “Use OAuth” chooses a mechanism but says little about authorization policy. Accessibility and localization apply to human-facing documentation, error guidance, and developer portals as well as graphical clients.

Quality attributes conflict. Strong consistency may increase latency or reduce partition availability. Verbose diagnostics may leak information. Long retention aids audits but increases privacy exposure. Record the decision owner and priority rather than pretending every quality can be maximized simultaneously.

### Treat failure and ambiguity as contract behavior

Specify which failures are distinguishable, retryable, terminal, or potentially committed. A client timeout is an observation, not a rollback. If duplicate effects are unacceptable, requirements must address operation identity, replay windows, lookup, and authoritative recovery. If work is asynchronous, define acceptance, status progression, terminal outcomes, cancellation, and retention.

Errors require stable machine meaning, human guidance, correlation, and disclosure policy. Do not expose whether a secret resource exists merely because developers want precise diagnostics. Do not return success when requested work is silently dropped. Define partial success only when consumers can identify and recover each item's outcome.

### Move from requirements to candidate contract

Only after obligations stabilize should the team propose resources, methods, representations, status codes, events, and schemas. For every candidate element, ask which requirement it satisfies. Elements without a trace are speculative surface area; requirements with no contract or operational mechanism are gaps.

An OpenAPI description can make paths, operations, parameters, responses, schemas, and security declarations reviewable and testable. It cannot express every temporal, authorization, reliability, or business invariant. Keep those obligations in governed requirements and acceptance scenarios, linking them to the interface description and executable tests.

### Govern change and disagreement

Requirements evolve when evidence changes. Version decisions, rationale, source, and affected consumers. Resolve contradictions explicitly: one actor may demand immediate deletion while another requires statutory retention; one client may need strict ordering while throughput goals favor concurrency. The durable output is a recorded policy decision with consequences, not a compromise hidden in code.

Traceability is bidirectional. From a requirement, reviewers can find scenarios, contract elements, tests, telemetry, and owners. From an endpoint or schema field, reviewers can find the consumer need and compatibility consequence. Traceability supports impact analysis; it does not prove the original need was correct.

## Definitions and Notation

Let $A$ be actors, $O$ outcomes, $R$ requirements, $S$ acceptance scenarios, and $K$ candidate contract elements. Relation $N\subseteq A\times O$ records who needs which outcome. Relation $C\subseteq R\times S$ records scenario coverage. Relation $T\subseteq R\times K$ traces requirements to proposed interface elements.

A requirement $r$ is **uncovered** when no scenario can test it: $\{s\in S\mid(r,s)\in C\}=\varnothing$. A contract element $k$ is **unjustified** when no requirement traces to it: $\{r\in R\mid(r,k)\in T\}=\varnothing$. These are review signals, not automatic deletion rules: exploratory features and manual review obligations can be legitimate when explicitly governed.

A **precondition** is required before the stimulus. A **postcondition** is an externally meaningful state after the interaction. An **invariant** must hold across allowed transitions. A **fault model** states which failures a guarantee covers. A **service-level indicator** is a measured quantity; an objective sets a target over it. An **acceptance criterion** is a specific condition used to judge a requirement.

## Mechanisms, Invariants, or Proof Structure

Use this outside-in sequence:

1. Identify actors, capabilities, incentives, and trust boundaries.
2. State outcomes and failure consequences without endpoint language.
3. Gather evidence and classify facts, assumptions, constraints, policies, and preferences.
4. Split obligations into atomic functional and quality requirements.
5. Define measurement boundaries and acceptance oracles.
6. Build normal, boundary, failure, concurrency, recovery, and abuse scenarios.
7. Resolve contradictions and assign priorities and decision owners.
8. Propose the smallest contract that covers accepted requirements.
9. Trace requirements to contract elements, tests, telemetry, and operational controls.
10. Review with consumer, domain, security, reliability, and implementation perspectives.

The **outcome-first invariant** forbids a chosen endpoint from serving as its own rationale. The **observability invariant** requires mandatory behavior to have an attainable oracle. The **fault-model invariant** bounds guarantees to named conditions. The **minimal-surface invariant** challenges untraced public elements. The **ambiguity invariant** requires unknown or potentially committed outcomes to be represented honestly.

Coverage supports a limited argument: if every $r\in R$ has relevant scenarios and those scenarios pass, there is evidence for the declared requirements under the tested conditions. It does not establish that $R$ contains every real need, that scenarios span every execution, or that production conditions match the test environment.

## Alternatives and Trade-Offs

**Outside-in versus implementation-first.** Outside-in work reduces accidental coupling and exposes recovery needs early, but requires stakeholder time and explicit decisions. Implementation-first prototypes reveal feasibility quickly but often turn storage structures and framework defaults into public contracts. Use prototypes as evidence, not as unreviewed requirements.

**Narrative scenarios versus formal models.** Narratives are accessible and reveal human consequences. State machines, decision tables, and schemas expose gaps and contradictions more mechanically. Combine concise narratives with the smallest formal model that captures risky transitions.

**Contract-first versus code-first description.** Contract-first review can align consumers before implementation. Code-first generation reduces duplication and drift for implemented details. Neither discovers requirements automatically; both need a governed source of semantic obligations and compatibility review.

**One general API versus actor-specific views.** A single interface can reduce duplication but may leak data, expose confusing options, and couple actors with incompatible quality needs. Separate views improve least privilege and usability but add consistency and operational cost. Choose based on shared semantics and trust, not fashion.

## Failure Modes and Misconceptions

Requirements are not a wishlist, UI storyboard, backlog, schema, or test suite. HTTP compliance does not imply domain correctness. A generated OpenAPI file is not automatically an agreed contract. “Real-time,” “exactly once,” “secure,” and “available” are incomplete without models and boundaries. More fields are not free flexibility; every public field carries meaning, authorization, privacy, and compatibility obligations. Mock satisfaction does not prove production dependencies meet latency or recovery goals.

## Worked Examples

### Example 1

A stakeholder asks for `POST /customers/search`. The analyst asks what outcome is needed and learns that support agents must locate an account from an exact invoice number without seeing unrelated customers. The resulting requirement covers an authorized exact lookup, bounded disclosure, and no result ambiguity. Method and path remain later design choices. **Conclusion:** translating the proposed endpoint back into outcome and constraints reveals the real obligation.

### Example 2

“Responses must be fast” cannot be falsified. Traffic evidence shows interactive clients need visible confirmation. The team writes: “For order lookups with representations at most 50 KiB under the declared regional load profile, 99% of server-observed response-header latency is at most 300 ms per rolling 30 minutes.” It separately budgets client-network latency. **Conclusion:** population, boundary, statistic, threshold, and window turn a preference into a reviewable objective.

### Example 3

A buyer submits an order, the server commits, and the response is lost. A happy-path requirement would permit an unsafe duplicate. The revised requirement gives the logical operation a client-stable key, defines the replay window, and provides authoritative lookup after ambiguous outcomes. **Conclusion:** failure analysis adds obligations that no success-only endpoint list exposes.

### Example 4

Product asks for “admins can refund any payment”; compliance says refunds above €10,000 require two distinct approvers. These are contradictory if “admin” means one principal. The team records thresholds, separation of duties, audit evidence, and exception owner before designing operations. **Conclusion:** explicit policy resolution is required; implementation must not silently choose a stakeholder.

### Example 5

A list requirement says “return all devices.” One tenant owns 12 devices; another owns 12 million. Scenarios add empty, one-page, boundary-page, concurrent insertion, deletion, stable ordering, and continuation-expiry cases. **Conclusion:** scale and change reveal pagination and consistency questions hidden by the word “all.”

### Example 6

A team copies `customer_internal_flags` from its database into a public schema “for flexibility.” No actor outcome or scenario uses it, and the field exposes fraud-processing state. The traceability review marks it unjustified and removes it. **Conclusion:** minimal public surface reduces privacy and compatibility liabilities.

### Example 7

The requirement “invalid users receive `404`” mixes identity and disclosure policy. Analysis separates unauthenticated, authenticated-but-unauthorized, inaccessible-existing, and unknown-resource cases, then records which distinctions callers may observe. **Conclusion:** error semantics must derive from threat and consumer needs, not one convenient status code.

### Example 8

A batch import accepts 999 rows and rejects one. Returning plain `200` hides the rejected effect; rejecting the whole batch violates a partial-processing requirement. The agreed contract requires per-item stable identity, outcome, retryability, and aggregate completion. **Conclusion:** partial success needs recoverable item-level semantics.

### Example 9

A partner demands “exactly once delivery.” The transport can retry and connections can fail after receipt. The requirement is reframed as one durable business effect per operation identity within a stated retention window, with replay and lookup behavior. **Conclusion:** specify the observable domain invariant, not an impossible unbounded transport slogan.

### Example 10

An OpenAPI description validates and generated clients compile, but cancellation of an already shipped order has no declared outcome. A state-transition scenario exposes the omission even though syntax tooling passes. **Conclusion:** description validation checks representation of a contract, not completeness of requirements.

## Cross-Program Connections

[Tracing a Request Through Client, Proxy, and Service](010-tracing-a-request-through-client-proxy-and-service.md) supplies evidence limits, while [Resources, Representations, and Messages](001-resources-representations-and-messages.md) supplies the interface model that requirements will constrain. The next module, Resource Identification, turns accepted outcomes into resource boundaries. Software Requirements Engineering owns elicitation and traceability; Security Engineering owns threat-driven disclosure constraints; Software Testing and Quality Engineering owns acceptance design; Distributed Systems owns fault models and ambiguous outcomes.

## References

1. ISO/IEC/IEEE, *29148:2018 Systems and software engineering—Life cycle processes—Requirements engineering*, published second edition, November 2018; ISO records a third-edition DIS under development. Checked 2026-09-01. https://www.iso.org/standard/72089.html
2. R. Fielding, M. Nottingham, and J. Reschke, *RFC 9110: HTTP Semantics*, Internet Standard 97, June 2022, especially Sections 3, 9, and 15. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
3. OpenAPI Initiative, *OpenAPI Specification 3.2.0*, 19 September 2025, especially Sections 2 and 4. Checked 2026-09-01. https://spec.openapis.org/oas/v3.2.0.html

## Exercises

### Exercise 1

Classify each statement as outcome, requirement, assumption, constraint, policy, or design choice: (a) “use `PUT /profiles/{id}`,” (b) “the identity provider clock differs by at most five seconds,” (c) “only the account owner may change the payout destination,” and (d) “a verified owner can recover after a lost update response without applying the change twice.”

### Exercise 2

Rewrite “the search API must be fast, secure, and return every matching record” into separate testable requirements. State at least one measurement boundary, authorization rule, pagination/consistency rule, and failure behavior.

### Exercise 3

Construct a scenario matrix for cancelling a delivery. Include not found, unauthorized, queued, in transit, delivered, concurrent dispatch, repeated cancellation, and dependency timeout. Identify the authoritative postcondition for each class.

### Exercise 4

Compare a single broad customer API with separate customer-self-service and support-agent views. Evaluate authorization, disclosure, usability, duplication, consistency, and evolution.

### Exercise 5

A medical-device client can be offline for 48 hours and may retry an update after losing the response. Derive outside-in requirements for safe operation, freshness, conflict handling, audit, and recovery without selecting endpoints or payload schemas.

## Answers to the Exercises

### Answer 1

(a) is a design choice because it selects method and path. (b) is an assumption unless the API owner controls and guarantees that clock bound; it needs an owner and response when violated. (c) is an authorization policy. (d) is an outcome-oriented functional and recovery requirement; it still needs a replay window, identity rule, and acceptance oracle. A constraint would instead impose a non-negotiable boundary such as a statutory retention period.

### Answer 2

One model answer is: authorized callers can retrieve matching records without seeing records outside their scope; results use a stable declared ordering and continuation model under concurrent change; each page is bounded; invalid queries receive stable machine-readable rejection; and dependency failure never silently returns an incomplete result as complete. For a declared query/data/load profile, 99% of server-observed first-page response-header latency is at most an agreed threshold over a stated window. Acceptable alternatives may use snapshots or explicitly weaker consistency, but must define duplicates, omissions, expiry, maximum traversal, measurement boundaries, and evidence.

### Answer 3

Unknown and inaccessible deliveries follow the chosen disclosure policy. Queued delivery can transition authoritatively to cancelled. In-transit and delivered states reject cancellation or create a distinct return/interception request according to policy. Concurrent dispatch requires conditional state transition so only one terminal decision wins. Repeated cancellation should return the existing outcome rather than duplicate work. A dependency timeout yields an ambiguous attempt unless authoritative state lookup resolves it. Evaluation should verify every scenario states actor, precondition, stimulus, observable response, authoritative postcondition, retry rule, and disclosure constraint.

### Answer 4

A broad API centralizes semantics and can reduce duplicated implementation, but its schema and operations must safely serve the least-privileged actor; optional privileged fields invite disclosure mistakes and confusing contracts. Separate views can enforce least privilege and actor-focused language, yet risk divergent meanings and extra operational work. A strong design may share internal domain policy while publishing separate bounded contracts. The decision should follow materially different trust, outcome, and quality needs, with shared concepts and synchronization obligations documented.

### Answer 5

The device needs a durable logical-operation identity across at least the maximum offline/retry interval; a freshness rule for commands and device state; explicit rejection or reconciliation when the base state changed; bounded authorization that can be evaluated safely with stale credentials; an audit trail linking actor, device, intended change, attempts, and terminal outcome; and authoritative lookup after a lost response. The requirement must name safety invariants that remain local during disconnection, maximum tolerated clock uncertainty, conflict ownership, retention, and behavior when recovery evidence is unavailable. Endpoints and representations can be selected only after these obligations are accepted.
