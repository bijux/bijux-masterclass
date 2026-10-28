# Reference Answers — Module 01: Reliability Model and Critical Journeys

Read after attempting all twelve Reliability Model and Critical Journeys exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is process uptime not a user-journey SLI?

**Answer.** A process can answer probes while downstream work, durable state, or required outputs fail. Journey evidence includes all stages necessary for the outcome.

## 2. Define the eligible population for run-start freshness.

**Answer.** Runs durably accepted and committed with a job are eligible. Rejected or rolled-back submissions are not. Cancellation after acceptance is classified separately.

**Common mistake.** Defining “Define the eligible population for run-start freshness.” without a population, owner, threshold, or time window.

## 3. Should an invalid bearer token count against API availability?

**Answer.** Normally no when authentication correctly rejects it. A regression rejecting valid tokens is service-owned and must count through valid-credential classified traffic.

**Common mistake.** Giving an unconditional answer to “Should an invalid bearer token count against API availability?” without classifying responsibility and failure semantics.

## 4. What is the decisive oracle for artifact completion?

**Answer.** A consistent terminal run, completed job, immutable artifact metadata, matching content checksum, completion event, and required outbox record.

## 5. How should low traffic affect an SLO conclusion?

**Answer.** Report insufficient data or use a longer window; do not infer perfect reliability from zero eligible events.

**Common mistake.** Describing a procedure for “How should low traffic affect an SLO conclusion?” without a falsifiable completion condition.

## 6. Distinguish a failure mode from a symptom.

**Answer.** A failure mode is a mechanism such as lease expiry; a symptom is an observation such as increasing run-start latency.

## 7. Why version SLI definitions?

**Answer.** Changing filters, exclusions, thresholds, or event semantics changes measurement. Versioning preserves reproducibility and historical comparison.

## 8. What makes a reliability requirement falsifiable?

**Answer.** It names a condition, scope, oracle, and threshold that can fail—for example a child deadline exceeding its parent.

## 9. When may telemetry be the only available evidence?

**Answer.** For some transient internal timing or path selection, but not for durable business effects; the limitation must be explicit.

## 10. Why keep security failures in the reliability model?

**Answer.** Security controls can regress availability and telemetry can leak data. Course 3 remains a predecessor constraint.

## 11. Trace critical-journey outcome classification in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/http.py` and `capstone/tracks/typescript-fastify/src/reliability/http.ts`. The required invariant is that eligible, good, bad, and excluded populations are defined before telemetry and tied to durable user outcomes.

## 12. Compare critical-journey outcome classification across Python and TypeScript

Both tracks must preserve this invariant: eligible, good, bad, and excluded populations are defined before telemetry and tied to durable user outcomes. The intentional difference is that data types differ; the same operation/status pair must receive the same classification.
