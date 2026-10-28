# Worked Answers — Module 01: Reliability Model and Critical Journeys

Use these solutions to audit your reasoning for **Reliability Model and Critical Journeys**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is process uptime not a user-journey SLI?

A process can answer probes while downstream work, durable state, or required outputs fail. Journey evidence includes all stages necessary for the outcome.

The chapter’s decisive distinction is this: A critical journey is an externally meaningful sequence such as submitting one analysis exactly once or retrieving a verified artifact. It crosses components and therefore cannot be represented by a single endpoint uptime percentage.

**Evidence.** Recompute good, bad, eligible, excluded, and missing populations from durable outcomes; then validate burn-rate windows, alert linkage, and the user-journey dashboard.

## 2. Define the eligible population for run-start freshness.

Runs durably accepted and committed with a job are eligible. Rejected or rolled-back submissions are not. Cancellation after acceptance is classified separately.

**Common mistake.** Defining “Define the eligible population for run-start freshness.” without a population, owner, threshold, or time window.

In the cumulative capstone, the rule becomes concrete: Apply Critical journey, Good, bad, eligible, excluded, Reliability invariant to this module’s capstone increment: Derive the reliability case for six Analysis Runs journeys and connect every reliability requirement to one failure mode and one verification. State one misleading green signal and the durable observation that would overrule it.

## 3. Should an invalid bearer token count against API availability?

Normally no when authentication correctly rejects it. A regression rejecting valid tokens is service-owned and must count through valid-credential classified traffic.

**Common mistake.** Giving an unconditional answer to “Should an invalid bearer token count against API availability?” without classifying responsibility and failure semantics.

A useful way to reason about the boundary is: Client-policy and validation failures are excluded because the service fulfilled the protocol correctly. Timeout, overload, and server failures remain eligible bad events because they represent unavailable service for a valid journey. The policy is explicit and shared by both implementations. """

## 4. What is the decisive oracle for artifact completion?

A consistent terminal run, completed job, immutable artifact metadata, matching content checksum, completion event, and required outbox record.

The implementation consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=01 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 5. How should low traffic affect an SLO conclusion?

Report insufficient data or use a longer window; do not infer perfect reliability from zero eligible events.

**Common mistake.** Describing a procedure for “How should low traffic affect an SLO conclusion?” without a falsifiable completion condition.

The important nuance is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=01 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

## 6. Distinguish a failure mode from a symptom.

A failure mode is a mechanism such as lease expiry; a symptom is an observation such as increasing run-start latency.

Under concurrency or failure, the distinction becomes: Apply Critical journey, Good, bad, eligible, excluded, Reliability invariant to this module’s capstone increment: Derive the reliability case for six Analysis Runs journeys and connect every reliability requirement to one failure mode and one verification. State one misleading green signal and the durable observation that would overrule it.

## 7. Why version SLI definitions?

Changing filters, exclusions, thresholds, or event semantics changes measurement. Versioning preserves reproducibility and historical comparison.

The design remains honest only if: A critical journey is an externally meaningful sequence such as submitting one analysis exactly once or retrieving a verified artifact. It crosses components and therefore cannot be represented by a single endpoint uptime percentage.

**Evidence.** Recompute good, bad, eligible, excluded, and missing populations from durable outcomes; then validate burn-rate windows, alert linkage, and the user-journey dashboard.

## 8. What makes a reliability requirement falsifiable?

It names a condition, scope, oracle, and threshold that can fail—for example a child deadline exceeding its parent.

The consumer-facing consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=01 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 9. When may telemetry be the only available evidence?

For some transient internal timing or path selection, but not for durable business effects; the limitation must be explicit.

The operational consequence is: Client-policy and validation failures are excluded because the service fulfilled the protocol correctly. Timeout, overload, and server failures remain eligible bad events because they represent unavailable service for a valid journey. The policy is explicit and shared by both implementations. """

**Evidence.** Follow one correlation and trace identity from HTTP through database, worker, storage, and webhook while verifying links, attempt identity, bounded attributes, and redaction.

## 10. Why keep security failures in the reliability model?

Security controls can regress availability and telemetry can leak data. Course 3 remains a predecessor constraint.

The strongest engineering interpretation is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=01 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 11. Trace critical-journey outcome classification in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/http.py` and `capstone/tracks/typescript-fastify/src/reliability/http.ts`. The required invariant is that eligible, good, bad, and excluded populations are defined before telemetry and tied to durable user outcomes.

The defect-oriented view is: Client-policy and validation failures are excluded because the service fulfilled the protocol correctly. Timeout, overload, and server failures remain eligible bad events because they represent unavailable service for a valid journey. The policy is explicit and shared by both implementations. """

## 12. Compare critical-journey outcome classification across Python and TypeScript

Both tracks must preserve this invariant: eligible, good, bad, and excluded populations are defined before telemetry and tied to durable user outcomes. The intentional difference is that data types differ; the same operation/status pair must receive the same classification.

Across the Python and TypeScript tracks, the invariant is: Client-policy and validation failures are excluded because the service fulfilled the protocol correctly. Timeout, overload, and server failures remain eligible bad events because they represent unavailable service for a valid journey. The policy is explicit and shared by both implementations. """
