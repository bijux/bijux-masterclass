---
module_id: API-029
program: API & Service Engineering
level: 1
module_number: 29
title: Mocking and Consumer Exploration
status: complete
last_verified: 2026-09-01
---

# Mocking and Consumer Exploration

## One-Page Review

### Governing question

How can a team use API mocks to let consumers explore a proposed interface early, collect decision-quality feedback, and test bounded client behavior without mistaking scripted simulation for provider conformance?

### Essential definitions

- A **mock API** is a controlled substitute that maps requests and scenario state to programmed responses.
- A **stub** supplies predetermined responses at a dependency boundary; a mock often adds expectations, matching, or interaction verification.
- **consumer exploration** is structured use of a candidate interface to discover usability, semantic, integration, and compatibility problems before release.
- A **scenario** is an ordered or state-dependent set of exchanges representing one consumer situation.
- A **request matcher** selects a response from method, target, headers, content, actor context, and sometimes prior scenario state.
- **fidelity** is similarity to a target along named dimensions such as wire shape, protocol semantics, state transitions, timing, or failure behavior.
- An **oracle** is the expected classification or observation used to judge the consumer or mock interaction.

### Central model, mechanism, or theorem

Model a mock as $M:(q,s,c)\mapsto(r,s')$, where request $q$, scenario state $s$, and controlled context $c$ yield response $r$ and next state $s'$. Let fidelity vector $F(M)=(f_w,f_p,f_b,f_o)$ cover wire, protocol, behavioral, and operational dimensions. A high value in one coordinate does not imply another: schema-valid bodies do not prove correct statuses, state transitions, authorization, latency, or provider behavior. Every mock result must therefore name the modeled dimensions and omitted evidence.

### Critical invariants

Fixtures trace to a reviewed contract version and consumer question. Matching uses only contractually meaningful request properties. Defaults never conceal missing scenario coverage. Success, failure, boundary, authorization, retry, and state cases are explicit. Dynamic values are deterministic or constrained by predicates. The mock rejects unsupported requests instead of inventing plausible success. Consumer observations become reviewed contract decisions or tracked questions. Mock and provider tests share fixtures where useful but retain different evidence labels. Secrets, personal data, production callbacks, and uncontrolled external effects are absent.

### Common failures

Returning `200` for every request; matching only path and ignoring method, media type, headers, or body; examples that violate schemas; one happy-path fixture; stateful behavior hidden in global mutable state; random IDs and sleeps; perfect success that teaches no recovery; simulated authorization based only on token presence; echoing untrusted input; permissive fallbacks; consumer code coupled to fixture IDs or property order; mock servers accessible with internal data; and claiming that a passing mock test proves the real provider works.

### Compact example

A consumer submits `POST /orders` to a scenario mock. A valid request returns `201`, `Location`, and a stable order; the same idempotency identity returns the same order; an invalid quantity returns a problem response; an unknown route returns an explicit unmatched-request diagnostic. The consumer discovers that it needs `Location` and a stable problem type. **Conclusion:** the mock accelerated a contract decision and client implementation, but provider execution must still verify effects and policy.

### Connections

[Examples and Executable Documentation](027-examples-and-executable-documentation.md) supplies safe fixtures. [Contract-First and Code-First Workflows](028-contract-first-and-code-first-workflows.md) supplies authority and provenance. [Reviewing a Contract for Ambiguity and Incompleteness](../ROADMAP.md) turns exploration findings into systematic review. Later modules on Contract Testing and Integration Testing distinguish provider and end-to-end evidence.

## Governing Question

Which mock architecture, scenarios, matchers, feedback practices, and evidence boundaries allow consumers to learn early while preventing false confidence and mock-specific coupling?

## Why This Matters

Consumers often cannot wait for a complete provider. They need to evaluate names, task flow, request construction, pagination, errors, generated clients, retries, and integration boundaries while change is still inexpensive. A contract-driven mock turns a proposed description and examples into an interactive surface. It lets a mobile developer, partner team, or command-line client discover questions that static review misses.

The value comes from feedback, not imitation for its own sake. A mock can reveal that a required identifier is unavailable at call time, an error lacks recovery information, pagination cannot resume, or a response forces three unnecessary calls. Those are design findings. The mock is useful even if its implementation is deliberately small.

False confidence is the central hazard. A mock can return a valid response without executing authentication, authorization, transactions, concurrency control, side effects, queues, databases, or downstream failures. It can be more deterministic and available than production. Consumers may pass against it while failing on header casing assumptions, content negotiation, unknown fields, latency, or partial failures. The team must state exactly what the mock models and preserve a path from exploratory evidence to provider evidence.

## Prerequisites and Retrieval

Retrieve API requirements, HTTP request and response semantics, OpenAPI operations and examples, JSON Schema validation, media-type and parameter serialization, error contracts, idempotency, authentication and authorization, state machines, deterministic testing, fixtures, client parsing, compatibility, contract-first and code-first provenance, and safe test environments.

Before building a mock, retrieve the candidate contract digest, intended consumer task, scenario preconditions, actor capability, matching rules, state transitions, supported outcomes, permitted nondeterminism, data classification, network exposure, feedback owner, and provider verification plan.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish stubs, mocks, simulators, sandboxes, and real providers;
2. design contract-derived request matching and deterministic responses;
3. model stateful workflows, failures, authorization, retries, and time;
4. conduct consumer exploration and convert observations into contract decisions;
5. prevent fixture coupling, permissive fallbacks, unsafe data, and false confidence;
6. measure fidelity by named dimensions rather than a single realism claim; and
7. connect mock evidence to provider, compatibility, and deployment verification.

## Core Exposition

### Choose the substitute deliberately

Teams use “mock” for several different things:

- a **stub** returns canned data to keep a caller moving;
- a **mock** matches interactions and may assert expectations;
- a **fake** implements a simplified working substitute, such as an in-memory repository;
- a **simulator** reproduces selected protocol, state, timing, or failure behavior;
- a **sandbox** is a hosted, isolated environment that may contain real provider components; and
- a **record/replay proxy** captures exchanges and later replays them under explicit matching.

The names matter less than the evidence boundary. Document which layers are real, simplified, or absent. A schema-derived response generator may have broad shape coverage but no task semantics. A stateful simulator may model an order lifecycle but omit real authorization. A provider sandbox may execute production code with fake payment dependencies but use different deployment policy.

Start with the cheapest substitute that answers the current consumer question. Do not build a miniature duplicate provider when the question is whether a field name, error recovery link, or pagination cursor is usable.

### Derive behavior from governed artifacts

A contract-driven mock should consume the same reviewed contract artifact used by documentation and provider verification. Resolve references and validate it before starting the server. Record contract digest, mock version, configuration, fixture source, and enabled scenarios.

OpenAPI can supply operations, parameters, media types, schemas, examples, response statuses, headers, and security declarations. It cannot automatically supply every state transition, authorization decision, side effect, distribution, or timing rule. Add governed scenario fixtures rather than letting the mock invent behavior silently.

Generated schema examples are suitable for broad exploratory shapes only when labeled. Random strings and numbers can satisfy constraints while teaching nonsense domain behavior. Public onboarding scenarios should use reviewed deterministic examples with meaningful relationships among IDs, totals, links, statuses, and state.

If a description has no example for a selected response, the mock may generate one for a clearly labeled fuzz or discovery mode. In strict mode, unsupported outcomes should fail configuration or return a diagnostic—not masquerade as authoritative behavior.

### Match requests at the right specificity

A request matcher can inspect:

- HTTP method and normalized target path;
- path, query, header, and cookie parameters under declared serialization;
- `Content-Type` and `Accept` negotiation;
- parsed body values and selected semantic predicates;
- actor or capability fixture identity;
- idempotency and conditional request headers; and
- current scenario state.

Matching too little returns success for invalid calls. Matching too much couples clients to incidental details. JSON object member order, insignificant whitespace, generated trace IDs, and header ordering are normally poor match keys. Method, path variables, media type, required semantic values, and preconditions often matter.

Separate parsing, validation, scenario selection, and response production. If no matcher applies, return an unmistakable mock diagnostic with candidate mismatch reasons. Do not fall through to the first success fixture. A strict unmatched result teaches the consumer which contract assumption failed.

For ambiguous matchers, either reject configuration or define deterministic priority based on explicit specificity. File order is a fragile hidden policy. Test overlap with boundary requests.

### Validate both directions

Validate requests against the exact operation, parameter serialization, media type, schema dialect, direction, and security preconditions being modeled. Then validate every mock response against its declared status, headers, media type, and schema before serving it.

This catches a damaging asymmetry: a mock may strictly reject consumer requests but emit stale invalid fixtures. Response validation should happen at fixture load time when possible so defects fail immediately rather than during a workshop.

Validation is not full semantics. A request with `end < start` may satisfy independent field schemas but violate a cross-field rule. A response total may not equal its lines. A `201` may omit `Location`. Add semantic predicates and HTTP coherence checks under explicit owners.

Negative scenarios distinguish layers. Malformed JSON is a parsing failure; an unsupported media type is negotiation; a shape violation is schema validation; a stale `If-Match` is a precondition; an inaccessible resource is authorization policy; a sold-out item is domain state. Returning one generic `400` for all of them teaches the wrong client recovery behavior.

### Model state only where the question needs it

Stateless mocks are simple and reproducible. They work for independent reads, request construction, response parsing, and many failure branches. Stateful scenarios are needed for create-then-read, lifecycle transitions, conditional updates, idempotency, polling, or webhook registration.

Represent state explicitly as a small state machine. For an order scenario:

$$
S=\{\text{absent},\text{accepted},\text{processing},\text{fulfilled},\text{cancelled}\}.
$$

Define transition function $\delta(s,q,c)=s'$ and response function $\rho(s,q,c)=r$. Reject undefined transitions. If cancel is valid only from `accepted` or `processing`, a request from `fulfilled` should produce the reviewed conflict outcome rather than reset the fixture.

Isolate state per scenario session, test process, tenant, or explicit token. Global state makes tests order-dependent and leaks one consumer's actions into another's exploration. Provide a safe reset that targets exactly one isolated namespace. Prefer fixture initialization over sequences whose only purpose is setup.

Do not implement an entire production state model speculatively. Model the transitions the contract claims and consumer task requires. Record omitted concurrency, persistence, and failure behavior.

### Control time, identity, order, and randomness

Dynamic realism often reduces learning. Random IDs make assertions brittle; wall-clock timestamps complicate replay; unordered collections hide or invent ordering promises; sleeps make state transitions flaky.

Use a fixture clock, deterministic IDs, seeded generation when random diversity is the purpose, and explicit ordering policy. Where values should vary, specify predicates: UUID syntax, timestamp within the scenario interval, opaque cursor non-emptiness, or stable equality across retry. Never wildcard a whole object just because one field changes.

For asynchronous scenarios, expose a controlled clock or advancement operation available only within the isolated mock. A consumer can observe `accepted`, advance the fixture, and observe `fulfilled` without relying on sleep. The mock must not teach a fixed production duration unless that bound is contractual.

### Explore failures systematically

Consumers need failure behavior before production most, because recovery architecture becomes expensive to retrofit. Create a scenario catalog across:

- malformed syntax and unsupported media types;
- missing, wrong-type, boundary, and cross-field validation;
- unauthenticated, forbidden, and concealed targets;
- not found, conflict, and failed precondition;
- rate and quota exhaustion;
- dependency unavailability and timeout;
- partial or stale data where the contract permits it;
- retryable and non-retryable problems;
- duplicate requests and lost responses; and
- asynchronous intermediate and terminal failure.

Each scenario names the consumer decision it tests: retry, refresh, correct input, ask for authority, show a stable message, poll, abandon, or reconcile. Injecting arbitrary `500` responses without a recovery contract produces noise rather than evidence.

Failure selection can use an explicit scenario header only in an isolated mock namespace, a scenario configuration endpoint, or fixture input. Do not teach consumers to send test-only controls to production. Keep control metadata outside public request models and make generated documentation clearly separate it.

### Model authorization without pretending to enforce it

A mock can represent actor capabilities and expected disclosure outcomes. It should not validate real production credentials or copy production policy data. Use synthetic actor fixtures such as `buyer_owns_order`, `buyer_other_tenant`, and `support_read_only` selected through the mock harness.

Checking that an `Authorization` header merely exists is not authorization fidelity. It can help a client learn where credentials go, but it says nothing about signature, issuer, audience, expiry, scope, object ownership, or revocation. Label those omissions.

Return the same public concealment behavior expected from the provider and assert that restricted fields are absent. Avoid rich diagnostic responses that teach consumers secrets unavailable in production. Put mismatch diagnostics in a separate local log or mock-control channel.

### Make the mock strict by default

A permissive mock optimizes apparent progress: unknown fields are ignored, unsupported routes return generic data, any token works, and any query returns the same page. It also trains invalid assumptions.

Strict mode should:

1. reject unknown operations and unsupported media types;
2. apply declared parsing and serialization;
3. validate requests and responses;
4. reject ambiguous scenario matches;
5. expose only documented outcomes;
6. isolate and constrain state; and
7. report actionable local mismatch diagnostics.

Optional exploratory modes can deliberately generate boundary data, inject declared failures, or tolerate a candidate extension. The mode must be visible in evidence so a lenient exploration run is not confused with strict contract testing.

The following bounded matcher demonstrates method/path/state selection, strict rejection, and deterministic transitions. It is not an HTTP server, schema validator, or provider test.

<!-- bijux-verify: {"id":"strict-scenario-matcher","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"create:201:accepted\nread:200:accepted\ncancel:204:cancelled\nrepeat_cancel:409:cancelled\nunknown:unmatched\n","stderr":""}} -->
```python
def dispatch(method, path, state):
    key = (method, path, state)
    transitions = {
        ("POST", "/orders", "absent"): (201, "accepted"),
        ("GET", "/orders/o-1", "accepted"): (200, "accepted"),
        ("DELETE", "/orders/o-1", "accepted"): (204, "cancelled"),
        ("DELETE", "/orders/o-1", "cancelled"): (409, "cancelled"),
    }
    return transitions.get(key)

state = "absent"
for label, method, path in [
    ("create", "POST", "/orders"),
    ("read", "GET", "/orders/o-1"),
    ("cancel", "DELETE", "/orders/o-1"),
    ("repeat_cancel", "DELETE", "/orders/o-1"),
]:
    status, state = dispatch(method, path, state)
    print(f"{label}:{status}:{state}")

result = dispatch("PATCH", "/orders/o-1", state)
print(f"unknown:{'unmatched' if result is None else 'matched'}")
```

The matcher deliberately has no default success. A production-quality mock would separately parse and validate messages, attach response bodies and headers, isolate state, and explain mismatch details.

### Prevent coupling to fixtures

Consumers can accidentally depend on a mock's incidental behavior: fixed ID `o-1`, stable array order, one exact timestamp, absent unknown fields, zero latency, case-sensitive header lookup, or a single error instance. Such clients pass locally and fail against real providers.

Vary contractually variable values across a controlled suite. Include unknown response fields where compatibility policy permits, multiple valid enum branches, zero/one/many collections, Unicode, maximum lengths, different header casing at the protocol adapter, and declared response alternatives. Keep each variation deterministic and tied to a purpose.

Do not randomize everything in every run. Unreproducible failures slow diagnosis and make consumers ignore the suite. Use named fixtures or record seeds and minimized cases.

Generated clients need special attention. A mock should exercise serialization at the wire boundary, not call generated model constructors directly on both sides. Otherwise matching client and mock generator assumptions can agree with each other while both disagree with the actual protocol.

### Conduct a structured exploration session

Give consumers a task, not a tour of endpoints. For example: “Create an order after a price changes, recover from a lost create response, and show the final status.” Supply the candidate artifact, mock identity, synthetic credentials, scenario controls, and known fidelity limits.

Ask observers to record:

- information unavailable when constructing the request;
- unclear names or units;
- unexpected round trips;
- ambiguous absence, null, empty, or default behavior;
- missing statuses, headers, links, or recovery fields;
- error information needed for a safe user decision;
- assumptions the client library was forced to make;
- accessibility and localization concerns; and
- behavior the mock could not credibly represent.

Classify every observation as contract defect, mock defect, documentation defect, consumer misunderstanding, implementation question, or out-of-scope request. Assign an owner and decision. Do not automatically encode every preference; reconcile it with other consumers, domain ownership, security, and compatibility.

Exploration evidence should include participant role, task, artifact digest, mock version and mode, scenarios attempted, observations, decisions, unresolved questions, and limitations. It is internal design evidence, not external validation unless named external reviewers actually participated and authorized attribution.

### Convert findings into governed change

A finding becomes durable only when it changes an authority or is explicitly rejected with rationale. Update the contract, examples, scenario fixtures, policy, or documentation; run semantic compatibility review; regenerate projections; and rerun affected exploration.

Do not patch the mock alone to make a consumer happy if the provider and contract will not adopt that behavior. That creates a false local API. Conversely, if the mock is wrong, fix its matcher or fixture without changing a correct contract.

Keep feedback traceable from observation to decision and verification. A useful chain is:

$$
\text{task}\rightarrow\text{observation}\rightarrow\text{decision}\rightarrow
\text{authority change}\rightarrow\text{provider evidence}.
$$

If the chain ends at observation, the learning may be lost. If it skips authority change, mock and documentation may diverge.

### Separate mock tests from provider tests

Reuse logical fixtures where it reduces duplication, but execute them through different adapters and label results differently. A consumer-against-mock test asks whether the consumer constructs and interprets selected exchanges. A provider test asks whether the provider accepts, emits, and enforces selected obligations. An end-to-end test asks whether integrated deployed components accomplish a task.

The same scenario may have three reports. Equality of fixture identity helps comparison, but the environments, observations, and claims differ. Never copy a green mock result into provider conformance evidence.

Provider verification should include behaviors the mock simplified: real middleware order, authentication mapping, authorization, transactions, concurrency, external effects, timeouts, resource limits, and deployment configuration. Production observation can detect additional drift but cannot exhaust the input space.

### Operate mocks safely

Mock payloads must be synthetic and non-sensitive. Do not record and publish production traffic as fixtures without governed minimization and data review; replacing names alone does not remove quasi-identifiers, secrets, internal hosts, signed URLs, or tenant relationships.

Bind local mocks to loopback by default. Hosted team mocks need authentication, network policy, quotas, tenant isolation, audit logs, expiry, and no production credentials. Control endpoints that force errors or reset state must never share trust boundaries with a real provider.

Do not allow arbitrary proxy destinations, callbacks, or template evaluation. An attacker could use a mock with ambient network access for server-side requests or data exfiltration. Allowlist any intentional egress and strip credentials on redirects. Bound bodies, state, logs, and fixture lifetimes.

Record/replay requires extra caution. Captured responses become governed sensitive artifacts, request matching can leak tokens, and stale captures can teach obsolete behavior. Prefer constructed fixtures; when capture is necessary, obtain authorization, minimize before persistence, classify access, and expire artifacts.

### Measure coverage without overclaiming

Track operations, statuses, media types, parameter encodings, schema branches, boundaries, roles, state transitions, retry cases, and failure classes. Let $C$ be the chosen category set and $K(e)\subseteq C$ categories covered by scenario $e$. The measured set is:

$$
C_M=\bigcup_{e\in E}K(e).
$$

This reports what the catalog addresses, not whether $C$ is complete or each oracle is correct. A 100% score over happy paths says little about authorization or recovery. Pair counts with risk review and consumer tasks.

Measure feedback outcomes too: ambiguities found before implementation, contract changes accepted, missing recovery paths, fixture defects, and unresolved provider questions. Avoid vanity counts such as number of mock endpoints or generated examples.

## Definitions and Notation

Let request $q=(m,u,h,b)$ contain method, target, headers, and body. Let $s\in S$ be isolated scenario state and $c$ controlled actor, clock, and fault context. A mock is:

$$
M(q,s,c)=(r,s')
$$

for defined request-state combinations; strict unmatched requests return a diagnostic outside the public provider contract rather than invented success.

Let fidelity be a vector $F(M)=(f_w,f_p,f_b,f_o)$ for wire representation, protocol semantics, behavior/state, and operational characteristics. Comparing mocks requires naming the coordinates; there is no defensible scalar “realism” without weights and purpose.

Let contract version $v$ and digest $d_v$ identify fixture authority. Observation $o$ supports only claim set $K_o$ in mock environment $e_M$. Provider evidence requires a distinct observation in provider environment $e_P$.

A **scenario control** selects state, actor, clock, or injected failure outside the public model. A **mismatch diagnostic** explains why no request matcher applied. **Fixture coupling** occurs when consumer correctness depends on non-contractual mock constants. **Strict mode** rejects requests or responses outside supported scenarios. **Exploratory mode** deliberately varies or relaxes a named dimension and labels the result.

## Mechanisms, Invariants, or Proof Structure

1. Start from one consumer task and reviewed contract digest.
2. Choose the least complex substitute that can answer the question.
3. Define fidelity dimensions and omissions before implementation.
4. Validate configuration, requests, and responses in both directions.
5. Match contractually meaningful properties and reject unmatched requests.
6. Model only required state transitions with isolated deterministic context.
7. Add recovery, authorization, boundary, retry, and asynchronous scenarios.
8. Run structured exploration and classify every observation.
9. Change governed authorities, review compatibility, and regenerate projections.
10. verify providers separately and bind evidence to artifacts and environments.

The central invariant is epistemic: every passing result carries an accurate claim boundary. A mock may prove that a consumer handled programmed exchange $e$ under configuration $c$; it does not prove that a provider will produce $e$ or that all valid exchanges are handled.

## Alternatives and Trade-Offs

Static examples are cheapest and easiest to review but do not exercise real parsing or control flow. An interactive stateless mock adds request construction and response parsing. A stateful simulator adds workflow learning at greater maintenance cost. A provider sandbox gives stronger implementation evidence but arrives later and may be expensive or unsafe.

Contract-generated responses provide breadth and update automatically, but values may be meaningless and behavior shallow. Hand-authored scenarios communicate intent and failures, but they can drift and cover fewer combinations. Combine generated discovery cases with reviewed public scenarios and strict validation.

Exact request matching catches accidental differences but overfits whitespace, order, and dynamic values. Broad matching reduces brittleness but can accept invalid consumers. Match exact protocol semantics and meaningful predicates while normalizing only contractually irrelevant variation.

Stateful mocks represent workflows but create isolation and ordering hazards. Stateless scenarios are reproducible but cannot demonstrate transitions. Use explicit per-session state only for questions that require it.

Local mocks are fast, private, and easy to reset. Hosted mocks support cross-team exploration but require security, lifecycle, and tenancy controls. Provider sandboxes may support realistic credentials and dependencies but need quotas, cleanup, cost controls, and clear differences from production.

Record/replay captures realistic bytes quickly but imports sensitive data, accidental behavior, and staleness. Constructed fixtures are safer and more intentional. Use recording only under authorization and governance, then treat the result as candidate evidence rather than unquestioned contract.

## Failure Modes and Misconceptions

- **“A mock is a fake provider.”** It is a substitute with selected fidelity; identify what is absent.
- **“Schema-valid examples are realistic.”** They may be structurally valid yet semantically meaningless or incoherent.
- **“Any unmatched request can receive a default response.”** Defaults conceal unsupported behavior and invalid clients.
- **“Path matching is enough.”** Method, serialization, media type, preconditions, body, actor, and state can change meaning.
- **“State makes a mock more accurate.”** Unnecessary global state creates order dependence without useful fidelity.
- **“Random values prevent coupling.”** Unrecorded randomness creates irreproducible failures; use named variation or recorded seeds.
- **“A token-shaped string models authorization.”** It does not model issuer, audience, capability, ownership, or disclosure policy.
- **“Failure injection means return `500`.”** Useful failures connect classification to a consumer recovery decision.
- **“The consumer passed, so the contract is implementable.”** The mock may omit provider and operational constraints.
- **“The provider passed the same fixture, so evidence is identical.”** Different adapters, environments, and observations support different claims.
- **“Recorded traffic is the best fixture.”** It can preserve secrets, personal data, incidents, and accidental behavior.
- **“More endpoints mean better coverage.”** Coverage categories and task outcomes matter more than endpoint count.
- **“Consumer feedback should always change the API.”** Reconcile observations with other consumers, security, domain meaning, and compatibility.
- **“Mocks can be public without risk because they are fake.”** They can expose contracts, fixtures, controls, network access, and internal data.
- **“Zero latency helps client development.”** It can hide timeout, cancellation, progress, and concurrency defects; add controlled operational cases.

## Worked Examples

### Example 1

**Situation:** A mobile team needs to render an order list before the provider exists. **Reasoning:** A stateless mock with empty, one-item, full-page, and next-cursor scenarios answers layout and parsing questions. State and payment simulation add no value yet. **Conclusion:** choose the smallest substitute aligned with the consumer task.

### Example 2

**Situation:** `GET /orders` and `POST /orders` share a path, but the matcher inspects only the path. **Reasoning:** A create request receives a list response, masking wrong client dispatch. Add method, negotiation, parameter, and body validation before scenario selection. **Conclusion:** matching must preserve operation semantics, not URL resemblance.

### Example 3

**Situation:** A mock response example validates as an `Order` but returns `200` after creation without `Location`. **Reasoning:** Schema validation covers the body only. Validate status and required headers against the operation and HTTP contract. **Conclusion:** response fidelity includes protocol metadata as well as shape.

### Example 4

**Situation:** Every request with any bearer string receives another tenant's order fixture. **Reasoning:** Replace token-presence matching with synthetic actor capabilities and return the reviewed concealment outcome for inaccessible objects. State that cryptographic credential verification remains absent. **Conclusion:** mocks can model public authorization decisions without pretending to enforce production identity.

### Example 5

**Situation:** A polling client sleeps five seconds because the mock always completes then. **Reasoning:** This teaches a non-contractual duration. Use a controlled clock with accepted, processing, terminal success, and terminal failure scenarios; assert documented retry hints or bounds only. **Conclusion:** deterministic time control should not invent production guarantees.

### Example 6

**Situation:** Consumer tests depend on order ID `o-1` and the first array element. **Reasoning:** Add named fixtures with different valid IDs and orderings, assert identity by relationships or predicates, and document any actual ordering contract. **Conclusion:** controlled variation exposes fixture coupling without random noise.

### Example 7

**Situation:** A create call times out after the mock records the order. **Reasoning:** On retry with the same idempotency identity, return the same logical order and keep one effect; with a different identity, create a second order. Let the consumer test reconciliation. **Conclusion:** failure scenarios should include postconditions, not just status codes.

### Example 8

**Situation:** Exploration reveals that a `409` body says only “conflict.” **Reasoning:** The consumer cannot decide whether to refresh, retry, or ask the user. Record the observation, design stable problem types and recovery metadata, update the contract and fixture, then obtain provider evidence. **Conclusion:** exploration has value when findings enter governed design.

### Example 9

**Situation:** A record/replay mock contains real email addresses, bearer tokens, internal hostnames, and signed callback URLs. **Reasoning:** Disable access, revoke exposed credentials, classify the incident, remove unsafe artifacts under policy, and replace them with constructed synthetic fixtures. **Conclusion:** realistic capture is not worth uncontrolled data and credential exposure.

### Example 10

**Situation:** Consumer-against-mock tests pass, while the provider returns an undocumented `502` through a gateway. **Reasoning:** The mock did not include deployment intermediaries or dependency failure. Add the outcome to review, decide the public error contract, verify provider and gateway behavior separately, and update recovery scenarios. **Conclusion:** mock success cannot close provider or deployment evidence gaps.

## Cross-Program Connections

[Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies test doubles, fixtures, oracles, partitions, and interaction risks. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies synthetic identities, data classification, authorization, network controls, and safe failure disclosure. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies retries, partial failure, time, ordering, and eventual observation. [Developer Experience in Platform Engineering](../../29-platform-engineering/ROADMAP.md) can host mock capabilities and self-service scenarios while API owners retain public meaning.

## References

1. OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/v3.2.0.html), especially Paths, Operation, Parameter, Media Type, Example, Responses, and Security Requirement Objects, 19 September 2025. Checked 2026-09-01.
2. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), Internet Standard, June 2022. Checked 2026-09-01.
3. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema: A Media Type for Describing JSON Documents, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-core), 16 June 2022. Checked 2026-09-01.
4. A. Wright, H. Andrews, B. Hutton, and G. Dennis, [*JSON Schema Validation: A Vocabulary for Structural Validation of JSON, Draft 2020-12*](https://json-schema.org/draft/2020-12/json-schema-validation), 16 June 2022. Checked 2026-09-01.
5. M. Nottingham, E. Wilde, and S. Dalal, [*RFC 9457: Problem Details for HTTP APIs*](https://www.rfc-editor.org/rfc/rfc9457.html), Standards Track, July 2023. Checked 2026-09-01.
6. M. Fowler, [*Mocks Aren't Stubs*](https://martinfowler.com/articles/mocksArentStubs.html), terminology and interaction-based testing trade-offs, 2 January 2007. Checked 2026-09-01.

## Exercises

### Exercise 1

Classify a canned JSON file, an expectation-based in-process dependency, an in-memory order service, a stateful HTTP simulator, a hosted provider test environment, and a recorded proxy by substitute type and evidence boundary.

### Exercise 2

Trace a create-read-cancel order scenario. Define matcher inputs, isolated states, response statuses and headers, deterministic IDs and time, undefined transitions, and reset behavior.

### Exercise 3

Diagnose a mock that accepts unknown fields, ignores `Content-Type`, returns the same `200` body for every status, shares global state, uses random IDs, and allows arbitrary callbacks. Prioritize corrections.

### Exercise 4

Design a consumer exploration session for cursor pagination and rate limiting. Specify tasks, fixtures, failure cases, observations, artifact identity, participant prompts, finding classification, and follow-up evidence.

### Exercise 5

A partner integration passes against a mock but fails in production under latency, unknown response fields, token expiry, and a gateway-generated error. Design a layered repair without turning the mock into a duplicate production system.

## Answers to the Exercises

### Answer 1

The canned JSON file is a stub and supports parsing of one fixture. The expectation-based in-process dependency is a mock and supports selected interaction assertions, not HTTP behavior. The in-memory order service is a fake and supports simplified domain paths without persistence fidelity. The stateful HTTP substitute is a simulator with selected wire, protocol, and state fidelity. The hosted provider environment is a sandbox whose evidence depends on which production components and policies it contains. The recorded proxy is record/replay evidence for captured exchanges only, with staleness and sensitive-data risks. Each result must name configuration and omitted layers.

### Answer 2

Start one session in `absent`. Match `POST /orders` on method, path, JSON media type, schema-valid body, actor, and idempotency identity; return `201`, `Location`, stable order `o-1`, and state `accepted`. Match `GET /orders/o-1` in `accepted` and return `200`; match `DELETE` in `accepted`, return `204`, and enter `cancelled`. A repeated delete returns the reviewed idempotent or conflict outcome; an undefined patch is unmatched. Use a fixture clock and per-session state. Reset validates the session identity and restores only that namespace to `absent`.

### Answer 3

First close the arbitrary-callback path and restrict network exposure because it can enable external requests or data leakage. Add strict operation, `Content-Type`, parameter, request, and response validation; reject unknown fields according to the contract. Select outcomes by explicit scenarios and validate status, headers, media type, and body together. Isolate state per test/session and make reset narrow. Replace unrecorded randomness with deterministic fixtures or recorded seeds and predicates. Finally add failure and boundary coverage; do not retain a permissive fallback.

### Answer 4

Give consumers tasks to traverse an empty collection, one page, a full page with cursor, final page, invalid cursor, changed collection, quota exhaustion, and recovery after the advertised interval. Pin contract and mock digests; use deterministic pages, opaque cursors, clock control, and stable problem types. Ask participants what state they retain, whether links or cursors are sufficient, how they distinguish terminal pagination, and how they schedule recovery. Classify findings into contract, mock, docs, consumer, or provider questions; assign owners; update authorities; run compatibility review; and later verify provider and gateway behavior separately.

### Answer 5

Add controlled latency and timeout/cancellation scenarios, unknown-field fixtures, token-expiry public outcomes, and the reviewed gateway problem response to the mock only where they support consumer recovery. Make the client use tolerant response parsing, bounded deadlines, correct reauthentication, and status/problem classification. Do not simulate every production dependency. Add provider integration tests for authentication middleware and unknown fields, gateway tests for translated errors, deployment tests for time budgets, and observability for unexpected outcomes. Bind each report to contract and deployment identity; mock evidence remains consumer evidence.
