---
module_id: PLAT-018
program: Platform Engineering
level: 1
module_number: 18
title: Feedback and Error Diagnostics
status: complete
last_verified: 2026-09-02
---

# Feedback and Error Diagnostics

## One-Page Review

### Governing question

How should a platform communicate validation, denial, conflict, failure, delay, partial success, and uncertainty so people and automation can take the safest next action while operators can diagnose the same occurrence without exposing secrets or implementation internals?

### Essential definitions

- **feedback** is timely information about what the platform received, decided, changed, observed, and expects next.
- An **error contract** is the stable machine and human representation of a failed or incomplete interaction, including classification, scope, correlation, safe action, and compatibility.
- A **diagnostic** is evidence used to explain and investigate an occurrence; it may require more privilege than the consumer-facing error.
- An **error code** is a stable programmatic category. A message is localized explanatory text and must not be the automation key.
- A **correlation identifier** links representations and telemetry for one interaction or operation; it is neither authentication nor proof of causation.
- **retryable** means the contract permits a repeat under named preconditions, delay, and identity rules. It does not mean retry immediately or forever.
- An **unknown outcome** means the platform cannot yet prove whether an effect occurred; it requires observation or reconciliation before replay.
- A **support bundle** is a deliberately scoped, redacted package of identifiers, states, versions, and evidence for escalation—not a raw dump of the consumer's environment.

### Central model, mechanism, or theorem

Model consumer-visible feedback as $Z=(K,S,R,T,C,A,E,N)$: stable kind/code $K$, summary $S$, reason and classification $R$, affected target or field $T$, correlation $C$, permitted action $A$, safe evidence $E$, and next-state semantics $N$. Map the same occurrence to privileged telemetry through correlation rather than returning stack traces. Correct feedback preserves uncertainty: accepted is not complete, timeout is not failure, and absence of a response is not permission to duplicate a consequential effect.

### Critical invariants

- Stable codes, types, status, and structured fields drive automation; messages serve people and may change or localize.
- Every error identifies the failed scope, applicable version, and whether any state may have changed.
- Retry guidance states idempotency, preconditions, delay/backoff, attempt limits, and observation required before replay.
- Authorization failures do not reveal restricted resource existence, policy internals, credentials, or sensitive comparison values.
- Correlation connects API, operation, CLI, portal, event, logs, traces, metrics, and support without becoming a secret or user identifier.
- User-facing feedback contains no stack trace, token, secret, connection string, sensitive payload, or unnecessary internal topology.
- Errors and status changes are textually identifiable, associated with affected controls, and programmatically announced where required.
- A platform measures recovery and correct outcomes, not the volume of error text, logs, or support links displayed.

### Common failures

Returning HTTP 200 with an error body; using one `INTERNAL_ERROR`; making clients parse English; blaming the user; saying “retry” after an uncertain non-idempotent mutation; revealing that a hidden resource exists; returning stack traces; generating a new correlation ID at every layer; logging secrets; showing a spinner after operation identity is lost; announcing every progress tick assertively; suppressing partial success; treating timeout as cancellation; offering a support link without transferable context; and measuring lower error counts while users silently abandon tasks.

### Compact example

A deployment request is accepted with operation `op-7` and correlation `corr-9`. The provider later times out after receiving the mutation. The operation becomes `Unknown`, not `Failed`; the UI says the outcome is not yet known, disables blind resubmission, and offers safe refresh and escalation. The controller reconciles by the same request identity, discovers that the provider created the deployment, verifies ownership and workload state, then publishes `Succeeded`. The developer sees one stable operation across CLI and portal; operators use `corr-9` to join redacted logs and traces without exposing provider credentials.

### Connections

Retrieve self-service state and guardrails from [PLAT-005](005-self-service-and-guardrails.md), team authority from [PLAT-009](009-platform-team-boundaries.md), journey states and outcome evidence from [PLAT-011](011-developer-journeys.md) and [PLAT-012](012-time-to-first-successful-deployment.md), CLI and portal presentation from [PLAT-013](013-command-line-interfaces.md) and [PLAT-014](014-web-portals.md), operation and resource semantics from [PLAT-015](015-apis-and-declarative-resources.md), and documentation and discovery from [PLAT-017](017-documentation-and-discoverability.md).

## Governing Question

What does the consumer need to know now, what may they safely do next, and what privileged evidence must an operator retrieve to distinguish the real cause without turning the error surface into a data leak?

Feedback begins before failure. Validation, authorization, preview, acceptance, progress, waiting, success, partial success, cancellation, and uncertainty all shape whether a consumer can form an accurate mental model. Error messages are one part of a state and recovery contract.

The platform should be honest at the boundary. It cannot promise that every failure has one cause, that every timeout did nothing, or that every downstream message is safe to reveal. It can provide stable categories, scoped evidence, current knowledge, and a permitted next action.

## Why This Matters

Poor errors convert platform complexity into consumer guessing. A person retries, changes unrelated inputs, opens a support ticket, or bypasses a guardrail. Automation scrapes messages, retries terminal failures, or silently treats partial results as complete. Operators then reconstruct the interaction from timestamps and incompatible logs.

RFC 9457 defines a standard problem-detail representation for HTTP APIs and explicitly frames it as interface detail rather than an implementation debugging channel. Stable problem types and occurrence identifiers can support clients and support correlation, but an API must still define domain-specific semantics, extensions, security, and compatibility.

gRPC defines canonical status codes and distinguishes malformed arguments, state-dependent preconditions, aborted concurrency, unavailable services, deadlines, and unknown errors. Google AIP-193 adds a structured error model and standard detail payloads. The reusable lesson is a bounded error vocabulary plus typed detail—not that HTTP and gRPC codes are interchangeable or sufficient for every domain.

OpenTelemetry's stable log data model and current correlation guidance connect log records with trace and resource context. Current exception conventions warn that exception messages can contain sensitive information. Telemetry helps operators investigate; it does not justify copying privileged attributes into consumer responses.

WCAG 2.2 requires detected input errors to be identified and described in text, provides criteria for correction suggestions and prevention, and requires certain status messages to be programmatically determinable without unnecessary focus changes. These requirements reinforce a general principle: feedback must be perceivable, associated with its context, and useful for recovery.

Current DORA platform guidance reports clear task-outcome feedback as strongly associated with positive platform experience. Diagnostic quality is therefore a product capability, not merely a logging concern.

## Prerequisites and Retrieval

Retrieve platform product boundaries, consumer research, cognitive load, self-service state, guardrails, capability ownership, team escalation, journey mapping, verified deployment outcomes, CLI process contracts, portal state, declarative resources, scaffolding operations, and documentation discovery from PLAT-001 through PLAT-017.

You should understand HTTP and RPC status, structured data, asynchronous operations, idempotency, optimistic concurrency, authentication and authorization, distributed failure, retries and backoff, logs, traces, metrics, events, accessibility, localization, privacy, incident response, support, and API compatibility.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish consumer feedback, stable error contracts, operator diagnostics, and internal exceptions;
2. classify validation, authentication, authorization, absence, conflict, precondition, quota, transient, dependency, unknown, and internal failures;
3. design protocol-appropriate machine errors with safe human summaries and field-level corrections;
4. specify retry, backoff, idempotency, observation, and unknown-outcome behavior;
5. correlate feedback across synchronous requests, durable operations, telemetry, events, and support;
6. redact and authorize diagnostics without destroying operational usefulness;
7. make error identification, suggestions, progress, and recovery accessible across channels; and
8. evaluate diagnostic quality using recovery, outcome, privacy, reliability, and support evidence.

## Core Exposition

### Design feedback across the entire interaction

Before submission, explain required inputs, consequences, defaults, permissions, estimates, and unknowns. During validation, associate each problem with the exact field or relation. At submission, distinguish rejected, accepted, and completed. For long work, return durable operation identity, current state, last evidence, progress only when meaningful, and a way to resume after disconnect.

Success feedback says what changed, where, for which version, and how it was verified. Partial success lists completed and incomplete scopes plus compensation or continuation. Cancellation distinguishes “request to cancel accepted” from “effect definitely stopped.” Timeout says which deadline expired and whether the outcome is known.

Avoid reassurance without evidence. “Done” after queue insertion is false. “Something went wrong” is unhelpful. “Provider unavailable; no mutation was attempted; retry after 30 seconds with the same operation key” supports a decision.

### Define a layered error contract

Model consumer-visible feedback as

$$
Z=(K,S,R,T,C,A,E,N),
$$

where $K$ is stable kind or code, $S$ a concise summary, $R$ reason and classification, $T$ affected resource, operation, or field, $C$ correlation, $A$ permitted recovery, $E$ safe evidence, and $N$ next-state semantics.

The machine layer contains protocol status, stable type/code, structured field violations, retry metadata, resource and operation references, correlation, and extension version. The human layer contains plain-language summary, context, consequences, corrective action, and support route. The operator layer contains authorized logs, traces, events, provider codes, stack traces, deployment versions, and deeper evidence.

Map layers by occurrence identity and trace context. Do not return operator detail merely because it already exists. A correlation ID lets support retrieve evidence; it does not grant access to it.

### Build a stable taxonomy

**Invalid input** is wrong independent of system state: malformed identity, unsupported syntax, impossible range. Identify every safely reportable field problem in one response when practical.

**Failed precondition** means valid intent cannot proceed in current state: dependency not ready, required approval absent, resource deleting. State the unmet predicate and how to observe or satisfy it.

**Conflict or aborted work** means concurrency or field ownership prevented the requested transition. Return current/expected version, conflict scope, and whether re-read and recompute is safe.

**Unauthenticated** means usable identity evidence is absent or invalid. **Unauthorized** means the authenticated principal lacks permission. Avoid revealing hidden target existence; the same external response may cover not-found and forbidden while privileged audit retains the distinction.

**Quota or rate limit** identifies the governing limit, scope, reset or retry time when safe, and request identity. Do not tell consumers to retry aggressively.

**Unavailable or dependency failure** describes a transient inability under a defined objective. **Deadline exceeded** describes elapsed waiting, not necessarily absence of effect. **Unknown** preserves insufficient information. **Internal** is a last-resort interface category with correlation, not a substitute for operator classification.

Use domain codes below protocol categories when clients need stable recovery decisions. Keep the vocabulary small, documented, versioned, and testable. Adding a code can break exhaustive clients even when the wire schema is unchanged.

### Preserve structured protocol semantics

For HTTP, use the appropriate status and representation semantics. RFC 9457 problem details can carry `type`, `status`, `title`, `detail`, `instance`, and extensions. A type URI identifies a problem class; an instance identifies an occurrence. Do not overload `detail` with stack traces or require clients to parse it.

For gRPC, return canonical status codes and typed detail messages according to the service contract. Preserve meaningful distinctions such as `INVALID_ARGUMENT`, `FAILED_PRECONDITION`, `ABORTED`, `RESOURCE_EXHAUSTED`, `UNAVAILABLE`, `DEADLINE_EXCEEDED`, and `UNKNOWN`.

CLI failure uses standard error output, documented exit codes, and machine-readable error mode. Portal forms associate inline errors with controls and summarize failures. SDKs expose typed errors without discarding protocol data. Events carry stable failure reason and operation identity. All channels project the same domain classification.

### Make field and policy errors correctable

Return a list of violations with stable path, reason code, constraint, and safe message. Distinguish absent, malformed, unsupported, mutually exclusive, out of range, unknown field, unresolved reference, policy denied, and cross-field invariant.

Paths follow a documented notation and refer to the consumer representation, not an internal database field. Preserve submitted values in the interface when safe. Move focus or provide a summary route to the first error without hiding the others. Associate text with each control and never signal error by color alone.

Policy denial explains the consumer-controlled decision they can change and links the applicable public policy. It should not reveal hidden rule internals, sensitive comparison values, another tenant's resources, or evasion detail. If no consumer action can resolve it, say who owns the next step.

### Specify retry and uncertainty

Retry is part of the operation contract. State whether the request is safe to repeat, which idempotency key or resource version to reuse, whether the server attempted an effect, which observations precede replay, and the maximum or deadline. Supply server-directed delay such as retry-after metadata when available; clients add bounded exponential backoff and jitter.

Never label a non-idempotent operation retryable merely because a transport error is transient. A response can be lost after the server or provider acted. Persist operation identity before effect, correlate downstream calls, and reconcile current state.

Use an explicit unknown outcome when neither success nor failure is proven. Safe actions include wait, query the durable operation, observe by request identity, or escalate. Creating a new request with a new key can duplicate resources, rotations, payments, or deletions.

The following synthetic classifier verifies that retry advice is limited to cases whose contracts permit it.

<!-- bijux-verify: {"id":"error-recovery-classification","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cases=8\nuser_actionable=4\nretryable=2\nunknown_outcomes=1\nunsafe_retry=0\nsecrets_exposed=0\n","stderr":""}} -->
```python
cases = [
    {"code": "invalid_argument", "action": "correct_input", "retry": False, "outcome": "no_effect", "detail": "region is unsupported"},
    {"code": "failed_precondition", "action": "satisfy_dependency", "retry": False, "outcome": "no_effect", "detail": "approval is required"},
    {"code": "aborted", "action": "reread_recompute", "retry": False, "outcome": "no_effect", "detail": "resource version changed"},
    {"code": "resource_exhausted", "action": "wait_for_quota", "retry": False, "outcome": "no_effect", "detail": "project quota reached"},
    {"code": "unavailable", "action": "bounded_retry_same_key", "retry": True, "outcome": "no_effect", "detail": "provider unavailable"},
    {"code": "throttled", "action": "retry_after_same_key", "retry": True, "outcome": "no_effect", "detail": "retry after 30 seconds"},
    {"code": "unknown", "action": "observe_same_operation", "retry": False, "outcome": "unknown", "detail": "provider response was lost"},
    {"code": "internal", "action": "contact_support", "retry": False, "outcome": "no_effect", "detail": "correlation corr-9"},
]
user_actions = {"correct_input", "satisfy_dependency", "reread_recompute", "wait_for_quota"}
secret_markers = ("password=", "token=", "BEGIN PRIVATE KEY", "connection_string=")
unsafe_retry = sum(case["retry"] and case["outcome"] != "no_effect" for case in cases)
print(f"cases={len(cases)}")
print(f"user_actionable={sum(case['action'] in user_actions for case in cases)}")
print(f"retryable={sum(case['retry'] for case in cases)}")
print(f"unknown_outcomes={sum(case['outcome'] == 'unknown' for case in cases)}")
print(f"unsafe_retry={unsafe_retry}")
print(f"secrets_exposed={sum(any(marker in case['detail'] for marker in secret_markers) for case in cases)}")
```

The cohort is synthetic. A real service must derive retryability from the operation, provider, idempotency, and observation contracts; a shared code such as unavailable cannot decide safety alone.

### Correlate requests, operations, and evidence

Create a public-safe occurrence or correlation identifier at the platform boundary and propagate it where protocols permit. Preserve incoming trace context under trust rules; do not accept arbitrary tenant values as authoritative internal identifiers. Link synchronous request, durable operation, resource generation, provider request, audit event, log, trace, and support record.

One user journey can contain several requests and traces. The durable operation ID remains the consumer anchor; trace and span IDs describe executions. Retries can share operation identity while having distinct attempt and trace identities. Make these relationships queryable.

Correlation is evidence of instrumentation, not proof that two events caused each other. Clock skew, sampling, missing propagation, fan-out, queues, and reused values complicate inference. Preserve source, time, and scope.

### Build diagnostics for operators

Structured logs record event name, time, severity, service/resource identity, deployment version, operation and correlation, sanitized principal or tenant scope, target, action, result, error code, dependency, and safe dimensions. Traces locate latency and dependency paths; metrics reveal rates and saturation; events explain notable state transitions. None replaces the others.

Record exception type and stack trace only in authorized telemetry when useful. Exception messages can contain sensitive input. Sanitize carriage returns, delimiters, markup, and untrusted values to prevent log injection. Bound sizes and cardinality so an attacker cannot exhaust storage or monitoring.

Protect diagnostic confidentiality, integrity, availability, retention, deletion, and access audit. Tokens, passwords, session identifiers, private keys, connection strings, health records, payment data, raw payloads, and higher-classification data generally do not belong in logs. Hashing is not anonymization when the domain is guessable.

Detect telemetry failure. If logging or tracing is unavailable, the platform should not claim evidence exists. Critical audit may require a fail-closed or durable local path; ordinary debug telemetry may degrade safely. State the policy.

### Present accessible human feedback

Use direct, non-blaming language: what happened, affected scope, what may have changed, what the consumer can do, and where to get help. Avoid internal jargon and false precision. Localize messages but keep codes, paths, and identifiers stable.

For forms, identify the item in error and describe the error in text. Offer a correction suggestion when known and safe. For consequential submissions, preview, check, confirm, or provide reversal according to the interaction and applicable accessibility requirements.

Status changes such as accepted, running, results returned, saved, failed, or validation updated must be programmatically determinable where required. Do not steal focus for routine updates or announce every progress tick. Use assertive alerts only for important time-sensitive conditions. Preserve messages long enough to perceive and revisit.

CLI messages work without color and respect terminal width; machine output excludes prose decorations. Portal errors survive refresh through durable operation state. Documentation links use stable codes and versions. Support channels accept copyable correlation without requiring screenshots.

### Design escalation and support bundles

Escalation says who owns the failure, when to escalate, expected response, and what safe context to provide. A platform dependency failure routes to the platform or provider owner; invalid application behavior should not be bounced without evidence.

Generate a support bundle only after preview and authorization. Include platform and client versions, resource and operation references, timestamps, stable codes, redacted configuration shape, relevant condition history, health summaries, and correlation links. Exclude secrets, full environment variables, home files, source, unrelated logs, and other tenants.

Give the consumer the bundle manifest and allow inspection where feasible. Sign or checksum evidence if integrity matters. Time-limit upload links and record access. A bundle is an aid, not consent to unrestricted collection.

### Test failure behavior as a contract

Contract tests assert protocol status, type/code, structured fields, field paths, retry metadata, state-change statement, operation identity, correlation, localization independence, redaction, and compatibility. Snapshot messages cautiously: prose can improve without breaking clients.

Inject invalid input, denied access, missing resource, stale version, field conflict, unmet precondition, quota, throttling, provider outage, deadline, response loss after effect, partial success, controller restart, telemetry outage, cancellation race, and internal exception. Verify each channel preserves the same domain semantics.

Test with screen readers, keyboard, zoom/reflow, high contrast, reduced motion, localized expansion, narrow terminals, JSON consumers, stale clients, and support workflows. Fuzz untrusted error content and large payloads. Confirm errors themselves cannot trigger script, terminal escape, log injection, or secret disclosure.

### Measure diagnostic quality

Track failure rate by stable code and journey, validation correction rate, retries to recovery, unsafe duplicate attempts, unknown-outcome duration, time to actionable diagnosis, support escalation, first-contact resolution, abandoned tasks, stale documentation links, correlation coverage, redaction findings, diagnostic availability, and task completion after error.

Do not reward teams for hiding or collapsing errors to reduce counts. Rising validation errors can reveal a confusing input contract; falling support tickets can mean better self-service or silent abandonment. Combine telemetry with journey research, ticket review, incident learning, accessibility testing, and privacy audits.

Set objectives by consequence. Unknown payment, stuck production deletion, denied credential revocation, and sandbox name validation require different urgency. Improve the highest-harm recovery paths first.

## Definitions and Notation

$Z=(K,S,R,T,C,A,E,N)$ models consumer-visible feedback through stable kind, summary, classification, affected target, correlation, permitted action, safe evidence, and next-state semantics.

Let outcome knowledge $o\in\{\mathrm{no\ effect},\mathrm{success},\mathrm{failure},\mathrm{partial},\mathrm{unknown}\}$. Retry safety is a predicate of operation semantics, request identity, and observation—not merely error code.

For occurrence $x$, let $c(x)$ be its public-safe correlation and $\tau(x)$ its trace context. Equal correlation supports joining evidence under scope and access rules; it does not by itself establish causality.

Let recovery time be $t_r-t_e$, from perceivable error at $t_e$ to verified safe outcome at $t_r$. A shorter interval is beneficial only when the resulting action and outcome are correct.

## Mechanisms, Invariants, or Proof Structure

Use a feedback-design loop: map interaction states; define domain taxonomy; map protocols and channels; specify structured details; design human recovery; define retry and uncertainty; propagate operation and correlation identity; instrument authorized diagnostics; redact; test failures and accessibility; connect support; measure recovery; learn from tickets and incidents; version and retire codes deliberately.

The code invariant keeps automation independent of prose. The scope invariant identifies what failed and what may have changed. The retry invariant prevents duplicated consequential effects. The uncertainty invariant forbids inventing terminal outcomes. The correlation invariant joins channels without granting access. The redaction invariant keeps privileged data out of consumer and lower-trust telemetry.

Adversarial review includes hidden-resource enumeration; policy oracle; message parsing; correlation guessing; forged trace context; CR/LF log injection; terminal escape; HTML/script in provider detail; secret embedded in exception; oversized field-error list; high-cardinality labels; retry storm; duplicate effect after lost response; cancellation after completion; stale portal state; screen reader never announces error; and support bundle collects unrelated tenant data.

## Alternatives and Trade-Offs

**One generic error** is easy to implement and hard to misuse programmatically. It destroys recovery, measurement, and support precision.

**Fine-grained domain codes** enable automation and targeted guidance. They expand compatibility surface and can leak implementation or policy distinctions.

**Return all field violations** reduces correction cycles. It costs validation work and can expose cross-field or authorization information.

**Fail fast on the first violation** is simple and bounded. It produces repetitive round trips and inaccessible correction loops.

**Detailed consumer diagnostics** can accelerate self-service. They increase security, privacy, stability, localization, and cognitive-load risk.

**Correlation-only public errors** minimize disclosure. They force avoidable support work when safe corrective information exists.

**Automatic retry** masks transient faults. It increases latency, load, synchronized storms, and duplication risk without idempotency and budgets.

**Manual retry** preserves consumer control. It transfers protocol complexity and may be inaccessible or error-prone under pressure.

## Failure Modes and Misconceptions

- **“The status code is the error contract.”** Domain classification, scope, action, evidence, and compatibility still matter.
- **“The message is for clients.”** Automation must use stable structured fields, not localized prose.
- **“Timeout means failed.”** The effect may have succeeded before the response or deadline.
- **“Transient means retryable.”** Operation identity and idempotency determine safe replay.
- **“More detail is more helpful.”** Internal topology, policy logic, or sensitive values can create harm.
- **“A correlation ID explains the cause.”** It locates evidence; diagnosis still requires interpretation.
- **“Logs are the source of truth.”** They can be sampled, delayed, malformed, lost, duplicated, or compromised.
- **“Redaction can happen later.”** Secrets may already have propagated to storage, alerts, exports, and support.
- **“An alert is accessible.”** It must be textually associated and programmatically conveyed without harmful interruption.
- **“Fewer errors mean a better platform.”** Consumers may abandon, bypass, or receive false success instead.

## Worked Examples

### Example 1

A portal returns “invalid request.” The contract instead lists `spec.region` with code `unsupported_value`, safe allowed jurisdictions, and a link to current policy; the form associates the text and preserves other inputs.

### Example 2

An unauthorized caller requests a hidden database. The external response does not distinguish absent from forbidden. Privileged audit records the actual decision, principal, policy version, target hash, and correlation under restricted access.

### Example 3

Two clients update one resource version. The loser receives `aborted`, expected and current versions, conflicting field ownership, and instructions to re-read and recompute—not a blind automatic retry.

### Example 4

A provider returns a credential in an exception message. The consumer receives stable dependency failure and correlation. Telemetry records a sanitized exception type and provider code; tests fail if the credential pattern reaches response or logs.

### Example 5

A create response is lost. The operation remains unknown and the retry button is disabled. Reconciliation finds the provider object by request key, adopts it after ownership verification, and completes the original operation.

### Example 6

A rate limit returns governing scope, current limit, reset time, and `Retry-After`. The SDK uses bounded jittered backoff with the same request identity and stops at its deadline instead of synchronized rapid retry.

### Example 7

A long migration completes three of five resources. Status lists verified completed resources, two failures with separate codes, compensation limits, and a resume operation. It does not collapse the batch to success or erase completed work.

### Example 8

A web form inserts error text but a screen reader receives no announcement. The implementation adds an error summary, field associations, focus strategy, and programmatically determinable status while avoiding an assertive alert for every keystroke.

### Example 9

Support previously asks for full environment output. A previewed bundle now includes versions, resource/operation IDs, condition history, redacted configuration keys, correlation links, and check results; it excludes values, tokens, source, and unrelated logs.

### Example 10

Error counts fall after all provider failures become `internal`. Recovery time and support escalations worsen. The team restores actionable dependency and uncertainty categories and evaluates verified recovery instead of a cosmetically small taxonomy.

## Cross-Program Connections

API engineering contributes protocol status, problem details, RPC codes, typed errors, versioning, and client behavior. Distributed systems contributes partial failure, deadlines, retries, idempotency, concurrency, and uncertainty. Observability contributes logs, traces, metrics, events, context propagation, sampling, and evidence quality.

Security contributes authorization non-disclosure, secret handling, log injection resistance, diagnostic access, retention, and audit. Accessibility and human-computer interaction contribute error identification, correction, status communication, focus, language, and cognitive load. Reliability contributes objectives, fault injection, incident response, escalation, and recovery.

Product management contributes journey outcomes and qualitative feedback. Organizational design defines ownership across consumer, platform, provider, security, and support. Data governance defines which diagnostic data may be collected, where it may flow, and when it must be deleted.

## References

- IETF, [RFC 9457: *Problem Details for HTTP APIs*](https://www.rfc-editor.org/rfc/rfc9457.html), July 2023. Standard problem-detail model, types, occurrences, extensions, HTTP integration, compatibility, and security considerations; obsoletes RFC 7807.
- IETF, [RFC 9110: *HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), June 2022. Method and status semantics, representations, validators, authentication, authorization, retry implications, and intermediaries.
- gRPC Project, [*Status Codes*](https://grpc.io/docs/guides/status-codes/), current documentation retrieved September 2, 2026. Canonical RPC codes and distinctions among invalid input, preconditions, aborts, exhaustion, deadlines, unavailability, and unknown errors.
- gRPC Project, [*Error Handling*](https://grpc.io/docs/guides/error/), current documentation retrieved September 2, 2026. Cross-language error status, network failure, cancellation, deadline, unavailable, unimplemented, and unknown behavior.
- Google, [*AIP-193: Errors*](https://google.aip.dev/193), current guidance retrieved September 2, 2026. Canonical status messages, codes, standard typed details, localization, retry, request information, and error compatibility.
- OpenTelemetry, [*Logs Data Model*](https://opentelemetry.io/docs/specs/otel/logs/data-model/), stable specification retrieved September 2, 2026. Common log representation, resource and instrumentation context, trace context, attributes, events, and exception fields.
- OpenTelemetry, [*Logging*](https://opentelemetry.io/docs/specs/otel/logs/), current specification retrieved September 2, 2026. Structured events and correlation by time, trace context, and resource context.
- OpenTelemetry, [*Semantic Conventions for Exceptions in Logs*](https://opentelemetry.io/docs/specs/semconv/exceptions/exceptions-logs/), current documentation retrieved September 2, 2026. Stable exception attributes, severity guidance, span correlation, stack traces, and sensitive-message warning.
- OWASP Cheat Sheet Series, [*Logging Cheat Sheet*](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), current guidance retrieved September 2, 2026. Interaction identifiers, event attributes, sanitization, sensitive-data exclusions, testing, protection, retention, and attacks on logs.
- W3C, [*Web Content Accessibility Guidelines 2.2*](https://www.w3.org/TR/WCAG22/), W3C Recommendation dated December 12, 2024. Error identification, labels, suggestions, prevention, status messages, and complete-process conformance.
- W3C Web Accessibility Initiative, [*Understanding Status Messages*](https://www.w3.org/WAI/WCAG22/Understanding/status-messages), current guidance retrieved September 2, 2026. Programmatically determinable success, result, waiting, progress, warning, and error messages without unnecessary focus change.
- DORA, [*Platform Engineering*](https://dora.dev/capabilities/platform-engineering/), updated January 12, 2026. Clear task-outcome feedback, logs, diagnostics, self-service independence, task success, and balanced platform measurement.

## Exercises

### Exercise 1

Design the error contract for an asynchronous deployment API. Cover validation, authorization, conflict, acceptance, provider failure, timeout after effect, partial success, cancellation, correlation, retry, status, and support.

### Exercise 2

Map one domain error consistently across HTTP problem details, gRPC status and details, CLI human and JSON modes, portal form and operation views, events, SDKs, logs, traces, and documentation.

### Exercise 3

Threat-model error and diagnostic surfaces for resource enumeration, policy disclosure, secrets, injection, forged correlation, retry storms, telemetry loss, support bundles, and cross-tenant access.

### Exercise 4

Design a test and measurement program that distinguishes fewer errors from better recovery. Include contract, fault-injection, accessibility, localization, privacy, support, and outcome evidence.

### Exercise 5

Transfer the model to a hospital laboratory-result delivery platform. Address invalid orders, authorization, patient ambiguity, partial delivery, duplicate risk, unknown receipt, clinical correction, accessibility, audit, escalation, and the boundary between technical diagnostics and clinical truth.

## Answers to the Exercises

### Answer 1

Use stable domain types beneath protocol categories and a durable deployment operation. Validation returns all safe field paths, codes, constraints, and corrections with no effect. Authorization avoids hidden-resource disclosure while privileged audit retains reason. A version or field-owner conflict returns current/expected state and requires re-read. Acceptance returns operation and correlation, not success. Provider rejection records a typed terminal dependency reason and safe remediation. A timeout after mutation becomes `Unknown`; the client observes the same operation and must not create a new key. Partial success lists verified subresults and resume or compensation limits. Cancellation reports requested, cancelling, cancelled, completed-before-cancel, or unknown. Status includes generation, freshness, reason, evidence, and next action. Support receives an authorized redacted bundle tied to correlation. Retry metadata appears only where the same identity and operation contract make replay safe.

### Answer 2

For a stale resource version, define domain code `resource_version_conflict`. HTTP uses an appropriate conflict response with RFC 9457 type, occurrence, target, expected/current version, and recovery extension. gRPC uses `ABORTED` plus a typed detail carrying the same fields. CLI human mode names the resource and says to re-read; JSON emits the stable structure and documented exit category. The portal retains edits, identifies the changed fields, and offers compare/reload rather than blind overwrite. The event and SDK preserve the domain code and operation identity. Logs and traces add authorized handler, deployment, storage, and latency evidence under the same correlation. Documentation is keyed by the stable code. Messages can localize; automation never parses them. No channel silently retries a consequential whole-resource update.

### Answer 3

Normalize absent and forbidden externally where existence is sensitive; keep decisions in restricted audit. Return only public policy reasons and consumer-controlled corrections. Apply allowlists and redaction before serialization and log emission; fuzz provider messages, CR/LF, terminal escapes, markup, and oversized values. Generate correlation at a trusted boundary, scope it, and treat incoming context as untrusted. Rate-limit and budget retries, provide jitter and server delay, and reconcile unknown outcomes before replay. Monitor telemetry delivery and state honestly when evidence is missing. Support bundles require preview, explicit scope, least-privilege retrieval, time-limited transfer, access audit, retention, and tenant isolation. Test caches, exports, alerts, and downstream analytics because redaction at the UI is too late.

### Answer 4

Contract tests cover every code, protocol mapping, structured field, state-change statement, retry metadata, correlation, extension version, localization independence, and old-client behavior. Fault injection covers invalid input, denial, conflicts, quota, throttling, dependency outage, response loss after effect, restart, partial success, cancellation races, telemetry outage, and internal exceptions. Accessibility testing covers textual identification, field association, error summaries, programmatic status, focus, keyboard, screen readers, zoom, contrast, and non-color meaning. Localization tests expansion, placeholders, stable codes, and terminology. Privacy and security tests scan responses, logs, traces, metrics, events, support bundles, caches, and exports for secrets, injection, excess data, and tenant leakage. Measure correction, verified recovery, unknown duration, unsafe duplicates, abandonment, escalation, first-contact resolution, correlation coverage, and redaction incidents. Interpret counts with interviews and incident/ticket review.

### Answer 5

Use stable technical codes for invalid order identifiers, unsupported message shape, unauthorized route, ambiguous patient match, unavailable receiver, duplicate message identity, unknown acknowledgement, and correction-link failure. Never expose another patient's existence or clinical content through an error. Persist clinical message and delivery-operation identity before transmission. A lost acknowledgement is `Unknown`; reconcile with the authorized receiver before retransmission, because duplicate delivery can harm. Partial delivery names technical destinations and states without claiming clinical review. Laboratory and clinical authorities own result correctness, release, interpretation, and correction; the platform owns transport status and evidence. Accessible interfaces identify errors textually, announce status appropriately, and preserve urgency without color alone. Audit is restricted, minimized, immutable as required, and correlated. Escalation separates technical routing support from patient-safety and clinical decision paths. Technical success never proves that the result was clinically understood or acted upon.
